from datetime import date
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
import openai
from .models import Script
from diaries.models import Diary
from .serializers import ScriptSerializer, ScriptTinySerializer, ScriptDetailSerializer


# /api/v1/scripts url에 접근했을 때 API
class Scripts(APIView):
    def get(self, request):
        # 현재 날짜를 가져와서 현재 날짜 기준 정렬된 script 목록을 보내주기.
        year = timezone.now().date().year

        return Response(self.make_list_dict(year))

    def make_list_dict(self, year):
        all_script_list = dict()
        # year년도에 해당하는 월별 스크립트
        for i in range(1, 13):
            scripts_queryset = self.get_object_date(year, i)
            serializer = ScriptSerializer(scripts_queryset, many=True)
            all_script_list[i] = serializer.data
        return all_script_list

    # 보고싶은 script들만 가져오기 위한 get_object() - 날짜
    def get_object_date(self, year, month):
        try:
            if year and month:
                return Script.objects.filter(
                    learningDate__year=year,
                    learningDate__month=month,
                    email=self.request.user,
                )
            elif year:
                return Script.objects.filter(
                    learningDate__year=year,
                    email=self.request.user,
                )
        except Script.DoesNotExist:
            raise NotFound

    # 보고싶은 script들만 가져오기 위한 get_object() - 제목
    def get_object_title(self, wanttitle):
        try:
            return Script.objects.filter(
                title__icontains=wanttitle, email=self.request.user
            )
        except Script.DoesNotExist:
            raise NotFound

    def post(self, request):
        year = request.data.get("year")
        month = request.data.get("month")

        if year and month is None:  # 연도만 요청받았을 경우
            return Response(self.make_list_dict(year))

        elif year and month:  # 연도와 월 모두 요청받았을 경우
            scripts_queryset = self.get_object_date(year, month)
            serializer = ScriptSerializer(scripts_queryset, many=True)
            return Response(serializer.data)

        # 해시태그를 입력하면 제목 별로
        elif request.data.get("title"):
            scripts_queryset = self.get_object_title(request.data["title"])
            serializer = ScriptSerializer(scripts_queryset, many=True)
            return Response(serializer.data)


# /api/v1/scripts/[pk] url에 접근했을 때 API
class ScriptDetail(APIView):
    def get_object(self, pk):
        try:
            return Script.objects.get(pk=pk, email=self.request.user)
        except Script.DoesNotExist:
            raise NotFound

    def get_diary(self, script, date):
        try:
            return Diary.objects.get(nowDate=date, user_email=self.request.user)
        except Diary.DoesNotExist:
            return None

    def get(self, request, pk):
        script = self.get_object(pk)
        serializer = ScriptDetailSerializer(script)
        return Response(serializer.data)

    def put(self, request, pk):
        script = self.get_object(pk)
        serializer = ScriptTinySerializer(
            script,
            data=request.data,
            partial=True,  # partial = True는 필수 항목을 수정하지 않아도 error안난다는 의미
        )
        if serializer.is_valid():
            updated_script = serializer.save()
            response_data = ScriptTinySerializer(updated_script).data

            # "show_expr" 값이 1인 경우 처리
            # openai.api_key = 'your-api-key'
            show_expr = request.data.get("show_expr", None)
            input_expr = request.data.get("input_expr", None)
            if show_expr == 1:
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"Rewrite the following sentence in a different way: '{input_expr}'",
                    max_tokens=60,
                )
                response_data["paraphrase"] = response.choices[0].text.strip()

            # "add_diary" 값이 1인 경우 처리
            add_diary = request.data.get("add_diary", None)
            if add_diary == 1:
                # 현재 날짜 가져오기
                current_date = timezone.now().date()

                # 같은 날짜의 Diary 가져오기
                diary = self.get_diary(updated_script, current_date)

                # Diary가 없다면 새로 생성
                if not diary:
                    diary = Diary.objects.create(
                        nowDate=current_date,
                        comment="",
                        user_email=request.user,
                    )

                # 생성된 diary와 script 연결
                diary.diaryContents.add(updated_script)
                diary.save()
                response_data["diary_added"] = True

            return Response(response_data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        script = self.get_object(pk)
        script.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

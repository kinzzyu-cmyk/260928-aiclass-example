import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st


def make_sales_data():
	return pd.DataFrame(
		{
			'월': ['1월', '2월', '3월', '4월', '5월', '6월'] * 3,
			'상품': ['노트북'] * 6 + ['태블릿'] * 6 + ['스마트폰'] * 6,
			'매출액(만원)': [320, 350, 390, 370, 430, 470, 180, 210, 205, 240, 260, 290, 410, 395, 440, 480, 510, 560],
		}
	)


def make_study_data():
	return pd.DataFrame(
		{
			'학생': [f'{number}번 학생' for number in range(1, 19)],
			'주간 학습 시간': [2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 4, 6, 8, 10, 3, 5, 7, 9],
			'시험 점수': [52, 58, 63, 65, 71, 76, 79, 84, 90, 55, 61, 74, 82, 93, 57, 68, 73, 87],
			'학습 방법': ['혼자 공부'] * 9 + ['그룹 공부'] * 9,
		}
	)


font_names = {font.name for font in font_manager.fontManager.ttflist}
korean_font = next(
	(name for name in ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'Noto Sans CJK KR'] if name in font_names),
	None,
)
if korean_font:
	plt.rcParams['font.family'] = korean_font
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid', font=korean_font)


st.title('데이터 시각화 라이브러리 비교')
st.caption('같은 예시 데이터를 matplotlib, seaborn, plotly로 각각 표현합니다.')

sales_tab, study_tab = st.tabs(['월별 상품 매출', '학습 시간과 시험 점수'])

with sales_tab:
	sales_data = make_sales_data()
	st.subheader('월별 상품 매출')
	st.write('세 상품의 월별 매출 변화를 비교하는 예시 데이터입니다.')
	st.dataframe(sales_data, hide_index=True, use_container_width=True)

	matplotlib_column, seaborn_column, plotly_column = st.columns(3)
	with matplotlib_column:
		st.markdown('**Matplotlib**')
		figure, axis = plt.subplots()
		for product, group in sales_data.groupby('상품', sort=False):
			axis.plot(group['월'], group['매출액(만원)'], marker='o', label=product)
		axis.set_title('상품별 월간 매출 추이')
		axis.set_xlabel('월')
		axis.set_ylabel('매출액(만원)')
		axis.legend(title='상품')
		figure.tight_layout()
		st.pyplot(figure)
		plt.close(figure)

	with seaborn_column:
		st.markdown('**Seaborn**')
		figure, axis = plt.subplots()
		sns.lineplot(
			data=sales_data,
			x='월',
			y='매출액(만원)',
			hue='상품',
			marker='o',
			ax=axis,
		)
		axis.set_title('상품별 월간 매출 추이')
		axis.set_xlabel('월')
		axis.set_ylabel('매출액(만원)')
		axis.legend(title='상품')
		figure.tight_layout()
		st.pyplot(figure)
		plt.close(figure)

	with plotly_column:
		st.markdown('**Plotly**')
		figure = px.line(
			sales_data,
			x='월',
			y='매출액(만원)',
			color='상품',
			markers=True,
			title='상품별 월간 매출 추이',
			labels={'월': '월', '매출액(만원)': '매출액(만원)', '상품': '상품'},
		)
		st.plotly_chart(figure, use_container_width=True)

with study_tab:
	study_data = make_study_data()
	st.subheader('학습 시간과 시험 점수')
	st.write('학생의 주간 학습 시간과 시험 점수, 학습 방법을 담은 예시 데이터입니다.')
	st.dataframe(study_data, hide_index=True, use_container_width=True)

	matplotlib_column, seaborn_column, plotly_column = st.columns(3)
	with matplotlib_column:
		st.markdown('**Matplotlib**')
		figure, axis = plt.subplots()
		for method, group in study_data.groupby('학습 방법', sort=False):
			axis.scatter(group['주간 학습 시간'], group['시험 점수'], label=method)
		axis.set_title('학습 시간과 시험 점수의 관계')
		axis.set_xlabel('주간 학습 시간(시간)')
		axis.set_ylabel('시험 점수(점)')
		axis.legend(title='학습 방법')
		figure.tight_layout()
		st.pyplot(figure)
		plt.close(figure)

	with seaborn_column:
		st.markdown('**Seaborn**')
		figure, axis = plt.subplots()
		sns.scatterplot(
			data=study_data,
			x='주간 학습 시간',
			y='시험 점수',
			hue='학습 방법',
			s=70,
			ax=axis,
		)
		axis.set_title('학습 시간과 시험 점수의 관계')
		axis.set_xlabel('주간 학습 시간(시간)')
		axis.set_ylabel('시험 점수(점)')
		axis.legend(title='학습 방법')
		figure.tight_layout()
		st.pyplot(figure)
		plt.close(figure)

	with plotly_column:
		st.markdown('**Plotly**')
		figure = px.scatter(
			study_data,
			x='주간 학습 시간',
			y='시험 점수',
			color='학습 방법',
			hover_name='학생',
			title='학습 시간과 시험 점수의 관계',
			labels={
				'주간 학습 시간': '주간 학습 시간(시간)',
				'시험 점수': '시험 점수(점)',
				'학습 방법': '학습 방법',
			},
		)
		st.plotly_chart(figure, use_container_width=True)

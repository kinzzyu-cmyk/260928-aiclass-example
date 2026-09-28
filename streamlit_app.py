from datetime import date, time

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='Streamlit 요소 갤러리',
    page_icon='🧩',
    layout='wide',
)


def make_sample_data():
    return pd.DataFrame(
        {
            '날짜': pd.date_range('2026-09-01', periods=8, freq='D'),
            '팀': ['Alpha', 'Beta'] * 4,
            '활성 사용자': [128, 96, 144, 112, 158, 121, 173, 139],
            '응답 시간(ms)': [240, 310, 215, 275, 198, 260, 185, 230],
            '만족도': [4.2, 3.8, 4.5, 4.0, 4.7, 4.1, 4.8, 4.4],
            '지역': ['서울', '부산', '대전', '인천', '서울', '부산', '대전', '인천'],
            'lat': [37.5665, 35.1796, 36.3504, 37.4563, 37.5665, 35.1796, 36.3504, 37.4563],
            'lon': [126.9780, 129.0756, 127.3845, 126.7052, 126.9780, 129.0756, 127.3845, 126.7052],
        }
    )


sample_data = make_sample_data()

st.title('🧩 Streamlit 요소 갤러리')
st.caption('입력 위젯부터 데이터 표시, 차트, 알림, 채팅까지 한 페이지에서 살펴보세요.')

with st.sidebar:
    st.header('사이드바 위젯')
    st.selectbox('예제 카테고리', ['전체', '입력', '시각화', '데이터'])
    st.multiselect('관심 요소', ['폼', '차트', '표', '알림'], default=['폼', '차트'])
    st.divider()
    st.caption('사이드바에도 입력 요소와 안내를 배치할 수 있습니다.')

inputs_tab, data_tab, display_tab, chat_tab = st.tabs(
    ['입력 위젯', '데이터 & 차트', '알림 & 레이아웃', '채팅']
)

with inputs_tab:
    st.header('입력 위젯', divider='gray')
    st.write('폼 안의 값은 제출 버튼을 눌렀을 때 한꺼번에 처리됩니다.')

    with st.container(border=True):
        with st.form('widget_gallery_form'):
            left, right = st.columns(2)
            with left:
                name = st.text_input('텍스트 입력', placeholder='이름을 입력하세요')
                note = st.text_area('여러 줄 입력', placeholder='메모를 남겨 보세요', height=100)
                category = st.selectbox('선택 상자', ['디자인', '개발', '데이터'])
                tags = st.multiselect('다중 선택', ['Python', 'Streamlit', 'Pandas', 'Altair'], default=['Streamlit'])
                chosen_date = st.date_input('날짜 선택', value=date.today())
                chosen_time = st.time_input('시간 선택', value=time(9, 30))
            with right:
                quantity = st.number_input('숫자 입력', min_value=0, max_value=100, value=42, step=1)
                rating = st.slider('슬라이더', min_value=0.0, max_value=5.0, value=3.5, step=0.5)
                priority = st.select_slider('단계 선택', options=['낮음', '보통', '높음', '긴급'], value='보통')
                layout = st.radio('라디오 버튼', ['목록', '격자'], horizontal=True)
                mode = st.segmented_control('세그먼트 선택', ['보기', '편집', '공유'], default='보기')
                enabled = st.checkbox('체크박스', value=True)
                notifications = st.toggle('토글 스위치', value=False)
                color = st.color_picker('색상 선택', '#2E86AB')

            submitted = st.form_submit_button('입력값 제출', type='primary')

    if submitted:
        st.success(f'{name or "이름 없음"}님의 입력을 받았습니다.')
        st.json(
            {
                '메모': note,
                '분류': category,
                '태그': tags,
                '날짜': chosen_date.isoformat(),
                '시간': chosen_time.isoformat(),
                '수량': quantity,
                '평점': rating,
                '우선순위': priority,
                '레이아웃': layout,
                '모드': mode,
                '사용': enabled,
                '알림': notifications,
                '색상': color,
            }
        )

    st.subheader('파일과 버튼')
    upload = st.file_uploader('파일 업로더', type=['csv', 'txt', 'json'])
    if upload is not None:
        st.info(f'업로드된 파일: {upload.name} ({upload.size:,} bytes)')
    button_col, download_col = st.columns(2)
    with button_col:
        if st.button('알림 띄우기', icon='🔔'):
            st.toast('버튼을 눌렀습니다.', icon='✅')
    with download_col:
        st.download_button(
            '예제 텍스트 다운로드',
            data='Streamlit 다운로드 버튼 예제입니다.\n',
            file_name='streamlit-example.txt',
            mime='text/plain',
        )

with data_tab:
    st.header('데이터 표시와 차트', divider='gray')
    metric_columns = st.columns(3)
    metric_columns[0].metric('활성 사용자', '1,284', '+8.2%')
    metric_columns[1].metric('평균 응답 시간', '238 ms', '-12 ms', delta_color='inverse')
    metric_columns[2].metric('만족도', '4.3 / 5', help='샘플 지표입니다.')

    st.subheader('차트')
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.line_chart(sample_data, x='날짜', y='활성 사용자', color='팀')
        st.bar_chart(sample_data, x='지역', y='만족도', color='팀')
    with chart_right:
        st.area_chart(sample_data, x='날짜', y='응답 시간(ms)', color='팀')
        st.scatter_chart(sample_data, x='활성 사용자', y='응답 시간(ms)', color='팀', size='만족도')

    st.subheader('표와 지도')
    st.caption('데이터 에디터는 셀을 직접 수정할 수 있습니다.')
    st.data_editor(sample_data, width='stretch', hide_index=True, num_rows='dynamic')
    table_col, map_col = st.columns(2)
    with table_col:
        st.write('읽기 전용 표')
        st.dataframe(sample_data, width='stretch', hide_index=True)
        st.write('정적 표')
        st.table(sample_data[['지역', '팀', '만족도']].head(4))
    with map_col:
        st.write('지도')
        st.map(sample_data[['lat', 'lon']], zoom=5)

    st.download_button(
        '샘플 데이터 CSV 다운로드',
        data=sample_data.to_csv(index=False).encode('utf-8-sig'),
        file_name='sample-data.csv',
        mime='text/csv',
    )

with display_tab:
    st.header('메시지, 상태, 레이아웃', divider='gray')
    message_left, message_right = st.columns(2)
    with message_left:
        st.success('작업이 완료되었습니다.')
        st.info('일반적인 안내 메시지입니다.')
        st.warning('확인이 필요한 내용을 표시합니다.')
        st.error('오류 상태를 사용자에게 알립니다.')
    with message_right:
        st.metric('처리 진행률', '72%')
        st.progress(72, text='예제 작업 진행 중')
        with st.status('예제 작업 상태', expanded=True) as status:
            st.write('데이터를 준비하고 있습니다.')
            st.write('결과를 화면에 표시합니다.')
            status.update(label='예제 작업 완료', state='complete')

    with st.container(border=True):
        st.subheader('컨테이너')
        st.write('컨테이너는 관련 요소를 한 영역에 묶습니다.')
        with st.popover('팝오버 열기'):
            st.write('버튼을 눌러 열고 닫는 작은 패널입니다.')
            st.checkbox('팝오버 안의 체크박스')
        with st.expander('확장 영역 열기'):
            st.code("st.write('Hello, Streamlit!')", language='python')
            st.latex(r'\sum_{i=1}^{n} x_i')

    st.subheader('마크다운과 구조화 데이터')
    st.markdown('**굵은 글씨**, *기울임*, 링크, 목록을 지원합니다.')
    st.json({'framework': 'Streamlit', 'widgets': ['button', 'slider', 'selectbox']})

with chat_tab:
    st.header('채팅 요소', divider='gray')
    st.caption('아래 입력창에 메시지를 보내면 데모 응답이 대화에 추가됩니다.')
    if 'demo_messages' not in st.session_state:
        st.session_state.demo_messages = [
            {'role': 'assistant', 'content': '안녕하세요. Streamlit 채팅 UI 예제입니다.'}
        ]

    for message in st.session_state.demo_messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    prompt = st.chat_input('메시지를 입력하세요')
    if prompt:
        st.session_state.demo_messages.append({'role': 'user', 'content': prompt})
        st.session_state.demo_messages.append(
            {'role': 'assistant', 'content': f'입력한 내용: {prompt}'}
        )
        st.rerun()
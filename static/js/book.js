let storyData = [];
let loadingSpinner;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function toggleLoading(show) {
    if (loadingSpinner) {
        if (show) {
            loadingSpinner.style.display = 'block';  // 로딩 스피너 표시
        } else {
            loadingSpinner.style.display = 'none';  // 로딩 스피너 숨기기
        }
    } else {
        console.error("loading_spinner를 찾을 수 없습니다.");
    }
}

function loadBook() {
    toggleLoading(true); // 로딩 시작

    let formData = new FormData();
    let uniqueKey = getCookie('unique_key');
    formData.append('unique_key', uniqueKey);

    console.log('POST 요청 보냄: /post/story');
    fetch('/post/story', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('POST 응답 받음: /post/story');
        if (data['load_book'] === true) {
            storyData = data;

            // 배경 이미지 설정
            document.querySelector('.story-container').style.backgroundImage = `url('../static/story_images/${storyData.image_path}')`;

            // 동화 제목 설정
            document.getElementById('story-title').innerText = storyData.title;

            // 동화 내용 설정
            document.getElementById('story-content').innerText = storyData.story;

            // 옵션 설정
            document.getElementById('option1').innerText = storyData.options[0];
            document.getElementById('option2').innerText = storyData.options[1];

            document.getElementById('option1').onclick = function() {
                toggleLoading(true);  // 옵션 클릭 시 로딩 스피너 표시
                getMakeBookStatus(storyData.options[0], uniqueKey);
            };

            document.getElementById('option2').onclick = function() {
                toggleLoading(true);  // 옵션 클릭 시 로딩 스피너 표시
                getMakeBookStatus(storyData.options[1], uniqueKey);
            };
        }
        toggleLoading(false); // 로딩 종료
    })
    .catch(error => {
        console.error('Error loading story:', error);
        toggleLoading(false); // 로딩 종료
    });
}

function getMakeBookStatus(selectedOption, uniqueKey) {
    let formData = new FormData();
    formData.append('unique_key', uniqueKey);
    formData.append('selected_option', selectedOption);

    console.log(`POST 요청 보냄: /post/makebookmore (option: ${selectedOption})`);
    fetch('/post/makebookmore', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('POST 응답 받음: /post/makebookmore');
        if (data['create_book'] === 200) {
            checkMakeBookStatus(uniqueKey, selectedOption);  // 상태 체크 시작
        } else {
            toggleLoading(false);   
            alert('요청을 처리하는 중 오류가 발생했습니다.');
        }
    })
    .catch(error => {
        console.error('Error during initial request:', error);
        toggleLoading(false);
    });
}

function checkMakeBookStatus(uniqueKey, selectedOption) {
    const interval = setInterval(() => {
        let formData = new FormData();
        formData.append('unique_key', uniqueKey);
        formData.append('selected_option', selectedOption);

        console.log(`POST 요청 보냄: /post/bookcp (option: ${selectedOption})`);
        fetch('/post/bookcp', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('POST 응답 받음: /post/bookcp');
            if (data['status'] === 'completed') {
                clearInterval(interval);  // 주기적인 요청 중지
                sendOptionAndReload(selectedOption, uniqueKey);  // 완료 후 책 로드
            }
        })
        .catch(error => {
            clearInterval(interval);
            console.error('Error checking status:', error);
            alert('상태 확인 중 오류가 발생했습니다.');
        });
    }, 5000);  // 5초마다 요청
}

function sendOptionAndReload(selectedOption, uniqueKey) {
    let formData = new FormData();
    formData.append('unique_key', uniqueKey);
    formData.append('selected_option', selectedOption);

    console.log(`POST 요청 보냄: /post/story (option: ${selectedOption})`);
    fetch('/post/story', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('POST 응답 받음: /post/story');
        console.log(data); // 응답 데이터 로그 출력

        if (data['load_book'] === true) {
            storyData = data;
            console.log('받은 storyData:', storyData);  // 받은 데이터를 확인

            // 화면 업데이트 (각 요소 업데이트 확인)
            document.querySelector('.story-container').style.backgroundImage = `url('../static/story_images/${storyData.image_path}')`;
            
            // 제목 업데이트
            let titleElement = document.getElementById('story-title');
            if (titleElement) {
                titleElement.innerText = storyData.title;
            } else {
                console.error("제목 요소가 없습니다.");
            }

            // 내용 업데이트
            let contentElement = document.getElementById('story-content');
            if (contentElement) {
                contentElement.innerText = storyData.story;
            } else {
                console.error("내용 요소가 없습니다.");
            }

            // 옵션 1 업데이트
            let option1Element = document.getElementById('option1');
            if (option1Element) {
                option1Element.innerText = storyData.options[0];
                option1Element.onclick = function() {
                    toggleLoading(true);  // 옵션 클릭 시 로딩 스피너 표시
                    getMakeBookStatus(storyData.options[0], uniqueKey);
                };
            } else {
                console.error("옵션 1 요소가 없습니다.");
            }

            // 옵션 2 업데이트
            let option2Element = document.getElementById('option2');
            if (option2Element) {
                option2Element.innerText = storyData.options[1];
                option2Element.onclick = function() {
                    toggleLoading(true);  // 옵션 클릭 시 로딩 스피너 표시
                    getMakeBookStatus(storyData.options[1], uniqueKey);
                };
            } else {
                console.error("옵션 2 요소가 없습니다.");
            }

        } else {
            console.error("책을 로드하는 데 실패했습니다.");
        }
        toggleLoading(false);  // 로딩 스피너 숨김
    })
    .catch(error => {
        console.error('Error reloading story:', error);
        toggleLoading(false);
    });
}

// DOM이 완전히 로드된 후 실행
window.onload = function() {
    loadingSpinner = document.getElementById('loading_spinner');
    loadBook();
};

const makeSubmit = document.getElementById('create_book');
const loadingSpinner = document.getElementById('loading_spinner');

makeSubmit.addEventListener('click', (e) => {
    loadingSpinner.style.display = 'block'; // 로딩 스피너 표시
    getMakeBook();
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}  

function getMakeBook() {
    let formData = new FormData();
    let uniqueKey = getCookie('unique_key');
    formData.append('unique_key', uniqueKey);

    fetch('/post/makebook', {
        method : 'POST',
        body : formData
    })
    .then(res => res.json())
    .then(data => {
        if(data['create_book'] === 200){
            checkMakeBookStatus();  // 첫 요청 성공 후 상태 확인 시작
        } else {
            loadingSpinner.style.display = 'none'; // 로딩 스피너 숨기기
            alert('다시 시도해주세요');  // 실패 시 메시지 표시
            location.reload();  // 페이지 새로고침
        }
    })
    .catch(error => {
        loadingSpinner.style.display = 'none'; // 로딩 스피너 숨기기
        alert('다시 시도해주세요');  // 에러 발생 시 메시지 표시
        location.reload();  // 페이지 새로고침
    });
}

function checkMakeBookStatus() {
    const interval = setInterval(() => {
        let formData = new FormData();
        let uniqueKey = getCookie('unique_key');
        formData.append('unique_key', uniqueKey);

        fetch('/post/bookcp', {
            method : 'POST',
            body : formData
        })
        .then(res => res.json())
        .then(data => {
            if (data['status'] === 'completed') {
                clearInterval(interval);  // 주기적인 요청 중지
                loadingSpinner.style.display = 'none'; // 로딩 스피너 숨기기
                location.href = '/book';  // 업로드 성공 시 페이지 이동
            }
        })
        .catch(error => {
            clearInterval(interval);  // 에러 발생 시 주기적인 요청 중지
            loadingSpinner.style.display = 'none'; // 로딩 스피너 숨기기
            alert('상태 확인 중 오류가 발생했습니다. 다시 시도해주세요.');
            location.reload();  // 페이지 새로고침
        });
    }, 5000);  // 5초마다 요청
}

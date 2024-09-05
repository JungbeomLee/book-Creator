function previewImage(event) {
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const noImageText = document.getElementById('noImageText');

    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewImg.style.display = "block";
            noImageText.style.display = "none";
        }
        reader.readAsDataURL(file);
    } else {
        previewImg.style.display = "none";
        noImageText.style.display = "block";
    }
}

// 쿠키 값을 가져오는 함수
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}  

const uploadSubmit = document.getElementById('upload_user_image_button');

uploadSubmit.addEventListener('click', (e) => {
    e.preventDefault(); // 기본 폼 동작 막기
    let uploadUserImages = document.getElementById('imageUpload').files;

    let formData = new FormData();
    formData.append('upload_image', uploadUserImages[0]);

    // 쿠키 값을 가져와 FormData에 추가
    let uniqueKey = getCookie('unique_key');
    formData.append('unique_key', uniqueKey);

    // 서버로 요청 보내기
    fetch('/post/image', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data['posting_image'] === true) {
            alert('성공!');
            location.href = '/createbook';  // 업로드 성공 시 페이지 이동
        } else {
            alert('Failed to upload image');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading the image.');
    });
});

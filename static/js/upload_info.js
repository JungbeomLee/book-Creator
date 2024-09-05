const uploadSubmit = document.getElementById('info_submit');

uploadSubmit.addEventListener('click', (e) => {
    function loadFetch() {
        e.preventDefault(); // 기본 폼 동작 막기
        const childName = document.getElementById('name').value.trim();
        const childAge = document.getElementById('age').value.trim();
        const childSex = document.getElementById('gender').value.trim();
        const childThema = document.getElementById('genre').value.trim();
        const childFavorite = document.getElementById('likes').value.trim();
        const childTeach = document.getElementById('teach').value.trim();

        // 유효성 검사
        if (!childName || !childThema || !childFavorite || !childTeach) {
            alert('모든 정보를 입력해주세요!');
            return; // 유효성 검사 실패 시, 이후 코드를 실행하지 않음
        }

        let user_Data = {};

        user_Data.childName = childName;
        user_Data.childAge = childAge;
        user_Data.childSex = childSex;
        user_Data.childThema = childThema;
        user_Data.childFavorite = childFavorite;
        user_Data.childTeach = childTeach;

        postName(user_Data);
    }

    loadFetch();
});

function postName(user_Data) {
    let postData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'name': user_Data['childName'],
            'age': user_Data['childAge'],
            'sex': user_Data['childSex'],
            'thema': user_Data['childThema'],
            'favorite': user_Data['childFavorite'],
            'teach': user_Data['childTeach']
        }),
    };
    fetch(`/post/info`, postData)
        .then(res => res.json())
        .then(data => {
            if (data['posting_name'] === true) {
                document.cookie = `unique_key=${data.unique_key}; path=/; max-age=3600; SameSite=Lax`;
                alert('성공!');
                location.href = '/upload/image';
            } else {
                alert('Failed to upload name&age');
            }
        });
}

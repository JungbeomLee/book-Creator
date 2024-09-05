let results = [];

function loadBook() {
    fetch('/get/story', {
        method: 'GET'
    })
    .then(res => res.json())
    .then(data => {
        if(data['load_book'] === true){
            results = data['story_list'];
            console.log('hi', results);
            renderFlipbook();  // Call the function to render the flipbook after the data is loaded
        }
    })
    .catch(error => console.error('Error loading book:', error));
}

function renderFlipbook() {
    const container = document.querySelector('.jch-flipbook-container');

    for (let i = 0; i < Math.floor(results.length / 2) + 1; i++) {
        const pageNum = i * 2;
        
        const flipbookPage = document.createElement('div');
        flipbookPage.className = "jch-flipbook-page";
        flipbookPage.setAttribute('data-page', pageNum.toString());

        if (i === 0) {
            flipbookPage.id = 'first';
        }

        const flipbookBack = document.createElement('div');
        flipbookBack.classList.add('jch-flipbook-back', 'jch-flipbook-theme', `jch-flipbook-theme-${i+1}`);
        if (i !== 0) {
            flipbookBack.setAttribute('data-page', (pageNum + 1).toString());
        }

        const flipbookFront = document.createElement('div');
        flipbookFront.classList.add('jch-flipbook-front', 'jch-flipbook-theme', `jch-flipbook-theme-${i}`);

        const flipbookOuterBack = document.createElement('div');
        flipbookOuterBack.className = 'jch-flipbook-outer';

        const flipbookContentBack = document.createElement('div');
        flipbookContentBack.className = 'jch-flipbook-content';

        const img1 = document.createElement('img');

        if (i === 0) {
            const h5 = document.createElement('h5');
            h5.textContent = results[0];
            img1.src = '../static/images/story_image/generated_image1.png';
            flipbookContentBack.appendChild(h5);
        } else {
            const p = document.createElement('p');
            p.textContent = results[pageNum];
            img1.src = `../static/images/story_image/generated_image${pageNum+1}.png`;
            flipbookContentBack.appendChild(p);
        } 
        img1.alt = '';
        flipbookOuterBack.appendChild(img1)
        flipbookOuterBack.appendChild(flipbookContentBack);
        flipbookBack.appendChild(flipbookOuterBack);

        const flipbookOuterFront = document.createElement('div');
        flipbookOuterFront.className = 'jch-flipbook-outer';

        const flipbookContentFront = document.createElement('div');
        flipbookContentFront.className = 'jch-flipbook-content';

        const img2 = document.createElement('img');

        if (i === 0) {
            const h5 = document.createElement('h5');
            h5.textContent = results[0];
            flipbookContentFront.appendChild(h5);
        } else {
            const p = document.createElement('p');
            p.textContent = results[pageNum - 1];
            img2.src = `../static/images/story_image/generated_image${pageNum}.png`;
            flipbookContentFront.appendChild(p);
        }

        img2.alt = '';
        flipbookOuterFront.appendChild(img2)
        flipbookOuterFront.appendChild(flipbookContentFront);
        flipbookFront.appendChild(flipbookOuterFront);

        if (i === 0) {
            flipbookPage.appendChild(flipbookBack);
            container.appendChild(flipbookPage);
        } else {
            flipbookPage.appendChild(flipbookFront);
            flipbookPage.appendChild(flipbookBack);
            container.appendChild(flipbookPage);
        }
    }

    const pages = document.querySelectorAll("[data-page]");
    const numPages = pages.length;
    let current = 1;

    function init() {
        sortZ();
    }

    init();

    const paperSound = new Audio('../static/js/paperSound.mp3');

    const prev = document.getElementById("jch-flipbook-prev");
    const next = document.getElementById("jch-flipbook-next");

    prev.addEventListener("click", prevPage);
    next.addEventListener("click", nextPage);

    function prevPage(event) {
        paperSound.play();
        current -= 2;
        if (current < 1) current = 1;
        turn(pages[current], 0);
        sortZ();
    }

    function nextPage(event) {
        console.log("next");
        paperSound.play();
        if (current < numPages - 1) turn(pages[current], -180);
        current += 2;
        if (current > numPages) current = numPages - 1;
        setTimeout(function () {
            sortZ();
        }, 1000);
    }

    function turn(page, angle) {
        page.style.transform = `rotateY(${angle}deg)`;
    }

    function sortZ() {
        for (let i = 0; i < numPages; i++) {
            pages[i].style.zIndex = (i > current + 1) ? 3 : 100 + i;
        }
    }
    
    const imgElements = document.querySelectorAll('.jch-flipbook-content');
    imgElements.forEach((img, index) => {
        img.addEventListener('click', (event) => {
            event.stopPropagation(); // 이벤트 전파 방지

            console.log(`Image ${index} clicked`)
        });
    });
}

window.onload = loadBook;
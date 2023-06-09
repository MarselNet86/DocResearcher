function initializeDocumentHandling() {
    const dropZone = $('#dropZone');
    const fileInput = $('#fileInput');
    const openFileButton = $('#openFileButton');
    const fileIcon = '<i class="fa-solid fa-file-import"></i>';
    const folderIcon = '<i class="fa-regular fa-folder fa-beat-fade"></i>';

    const toggleHighlightDropZone = (e) => {
        e.preventDefault();
        dropZone.toggleClass('highlight', e.type === 'dragover');
    };

    const handleFileDrop = (e) => {
        e.preventDefault();
        toggleHighlightDropZone(e);
        fileInput[0].files = e.originalEvent.dataTransfer.files;
        uploadFile(fileInput);
    };

    const handleFileChange = () => {
        uploadFile(fileInput);
    };

    const openFileSelection = () => {
        fileInput.click();
    };

    dropZone.on({
        dragover: toggleHighlightDropZone,
        dragleave: toggleHighlightDropZone,
        drop: handleFileDrop
    });

    fileInput.on('change', function () {
        const buttonText = $(this)[0].files.length === 0 ? `${fileIcon} Открыть файл` : `${folderIcon} Загрузка`;
        openFileButton.html(buttonText);
    });

    openFileButton.on('mousedown', function () {
        if (fileInput[0].files.length !== 0) {  // Если файл выбран
            $(this).html(`${fileIcon} Открыть файл`);
        }
    });

    openFileButton.on('mouseup', function () {
        if (fileInput[0].files.length === 0) {  // Если файл не выбран
            $(this).html(`${folderIcon} Загрузка`);
        }
    });

    $(window).on('focus', function () {
        if (fileInput[0].files.length === 0) {  // Если файл не выбран
            openFileButton.html(`${fileIcon} Открыть файл`);
        }
    });

    uploadFile(fileInput);
    fileInput.on('change', handleFileChange);
    openFileButton.on('click', openFileSelection);
}



function uploadFile(fileInput) {
    const file = fileInput[0].files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        const settings = {
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
        };

        let waitingBlock = `
            <div class='done-container'>
                <div class='done-block'>
                    <span class="done-text fa-fade">${file.name}</span>
                </div>
                <div class='waiting-block' id='countdown'>
                    Осталось: 1м 30с
                </div>
            </div>
        `;

        $('.documents-block').remove(); // Remove block with class "documents-block"
        $('.results-load').append(waitingBlock);
        $('.results-load').children().last().hide().fadeIn(); // Apply fadeIn() animation

        let countdownTime = 90; // Задаем начальное значение времени в секундах

        // Каждую секунду выполняем функцию
        let countdownInterval = setInterval(function () {
            countdownTime--; // уменьшаем время на 1 секунду
            let minutes = Math.floor(countdownTime / 60); // получаем количество минут
            let seconds = countdownTime % 60; // получаем количество секунд
        
            // проверяем, если время закончилось, обновляем текст на "Ожидайте..."
            if (countdownTime <= 0) {
                document.getElementById('countdown').innerText = "Ожидайте...";
                clearInterval(countdownInterval);
            } else {
                // обновляем текст обратного отсчета
                document.getElementById('countdown').innerText = "Осталось: " + minutes + "м " + seconds + "с";
            }
        }, 1000);
        

        $.ajax(settings).done(function (response) {
            // Remove waitingBlock
            $('.waiting-block').parent().remove();

        
            if (response.status === 'error') {
                console.log(response.error)
                let errorBlock = `
                    <div class='done-container'>
                        <div class='done-block'>
                            <span class="done-text">${file.name}</span>
                        </div>
                        <div class='error-block'>
                            Ошибка
                        </div>
                    </div>
                `;
        
                $('.results-load').append(errorBlock);
            } else {
                let downloadBlock = `
                <div class='done-container'>
                    <div class='done-block'>
                    ${file.name}
                    </div>
                    <a class='btn-download' href="/download/${response.zip_filename}_doc.zip">
                        <i class="fa-solid fa-arrow-down-long fa-bounce" style="color: #a0c157;"></i>Скачать
                    </a>
                </div>
                `;
        
                $('.results-load').append(downloadBlock);
            }
        });
    } else {
        console.log('Файл не выбран');
    }
}


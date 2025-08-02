document.addEventListener('DOMContentLoaded', function() {
    const menuUpload = document.getElementById('menu-upload');
    const uploadPreview = document.getElementById('upload-preview');
    const previewImage = document.getElementById('preview-image');
    const previewPdf = document.getElementById('preview-pdf');
    const replaceMenu = document.getElementById('replace-menu');

    menuUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();

        reader.onload = function(e) {
            if (file.type === 'application/pdf') {
                previewPdf.src = e.target.result;
                previewPdf.classList.remove('hidden');
                previewImage.classList.add('hidden');
            } else {
                previewImage.src = e.target.result;
                previewImage.classList.remove('hidden');
                previewPdf.classList.add('hidden');
            }

            uploadPreview.classList.remove('hidden');
        };

        reader.readAsDataURL(file);
    });

    replaceMenu.addEventListener('click', function() {
        menuUpload.value = '';
        uploadPreview.classList.add('hidden');
    });
});
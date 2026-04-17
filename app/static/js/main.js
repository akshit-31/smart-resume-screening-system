// File preview on upload page
const resumeInput = document.getElementById('resumes');
if (resumeInput) {
    resumeInput.addEventListener('change', function () {
        const fileList = document.getElementById('file-list');
        const filePreview = document.getElementById('file-preview');
        fileList.innerHTML = '';

        if (this.files.length > 0) {
            filePreview.classList.remove('d-none');
            Array.from(this.files).forEach(file => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.innerHTML = `
                    <span><i class="fas fa-file-pdf text-danger me-2"></i>${file.name}</span>
                    <span class="badge bg-secondary">${(file.size / 1024).toFixed(1)} KB</span>
                `;
                fileList.appendChild(li);
            });
        } else {
            filePreview.classList.add('d-none');
        }
    });
}

// Loading spinner on match form submit
const matchBtn = document.getElementById('match-btn');
if (matchBtn) {
    matchBtn.closest('form').addEventListener('submit', function () {
        matchBtn.disabled = true;
        matchBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2"></span>
            Analyzing Resumes... Please wait
        `;
    });
}

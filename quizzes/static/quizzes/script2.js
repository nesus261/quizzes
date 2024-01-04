document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.quiz-box-container').forEach(el => {
        el.addEventListener('click', () => {
            location.href = el.dataset.quizUrl;
        });
    });
});
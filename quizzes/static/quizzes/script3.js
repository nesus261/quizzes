document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#show-questions-button').addEventListener('click', function() {
        let questions_container = document.querySelector('.questions-container');
        if (questions_container.style.display == 'block')
        {
            questions_container.style.display = 'none';
            this.innerText = 'Show questions';
        }
        else 
        {
            questions_container.style.display = 'block';
            this.innerText = 'Hide questions';
        }
    });
    document.querySelector('#time-limit-switch').addEventListener('change', function() {
        if (this.checked)
        {
            document.querySelector('.time-container').style.display = 'block';
        }
        else 
        {
            document.querySelector('.time-container').style.display = 'none'; 
        }
    })
});
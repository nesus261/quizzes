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
    document.querySelector('#show-player-answers-switch').addEventListener('change', function() {
        if (this.checked)
        {
            document.querySelector('.show-answers-container').style.display = 'block';
        }
        else 
        {
            document.querySelector('.show-answers-container').style.display = 'none'; 
            document.querySelector('#show-correct-answers-switch').checked = false;
        }
    });
    /*
    document.querySelector('#time-limit-switch').addEventListener('change', function() {
        if (this.checked)
        {
            document.querySelector('.time-container').style.display = 'block';
        }
        else 
        {
            document.querySelector('.time-container').style.display = 'none'; 
        }
    });*/
    document.querySelector('#start-quiz-form').onsubmit = (e) =>{
        let fd = new FormData(e.target); 
        fetch('/init_game', {
            method: 'POST',
            body: fd
          })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            if (data.ok)
            {
                location.href = `/game/${data.code}`;
            }
            else if (data.message)
            {
                alert(data.message.body);
            }
          })
        return false;
    }
});
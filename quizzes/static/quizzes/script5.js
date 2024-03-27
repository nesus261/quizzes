class Socket {
    constructor() {
        this.server =  `ws://${window.location.host}/ws/game/${document.querySelector('#game-code').innerText}/`;
        this.socket = new WebSocket(this.server);
        this.init();
        
        this.questions = {};
    }
    init() {
        this.socket.onopen = () => {
            let id = getCookie('user_id');
            if (id)
            {
                let data = {
                    type: "new_user",
                    id: getCookie('user_id')
                };
                this.socket.send(JSON.stringify(data)); 
            }
            document.querySelector('#show-answers-button').addEventListener('click', (event) => {
                let answers_container = document.querySelector('.answers-container'); 
                answers_container.style.display = answers_container.style.display == 'block' ? 'none' : 'block';
                event.target.innerText = answers_container.style.display == 'none' ? 'Show answers' : 'Hide answers'
            });
        }
        this.socket.onmessage = (result) => {
            let data = JSON.parse(result.data);
            switch (data.type)
            {
                case "user_id":
                    setCookie('user_id', data.data);
                    this.init_wait_room();
                    break;
                case 'error':
                    let title = data.title || 'Error';
                    let reason = data.reason;
                    $('#messageModal .modal-title')[0].innerText = title;
                    $('#messageModal .modal-body')[0].innerText = reason;
                    $('#messageModal').modal('show');
                    break;
                case "start_game":
                    this.init_game_room();
                    break;
                case "question":
                    this.questions = data.data;
                    this.next_question();
                    break;
                case "end_quiz":
                    this.end_quiz(data.data);
                    break;
            }
        }
        document.querySelector('.username-form').onsubmit = (e) => {
            this.socket.send(JSON.stringify({
                type: "new_user",
                username: e.target.username.value
            })); 

            return false;
        };
    }
    init_wait_room() {
        document.querySelector('.username-room').style.display = 'none';
        document.querySelector('.wait-room').style.display = 'block';
    }
    init_game_room() {
        document.querySelector('.username-room').style.display = 'none';
        document.querySelector('.wait-room').style.display = 'none';
        document.querySelector('.game-room').style.display = 'block';
    }
    next_question() {
        document.querySelector('.question-number').innerText = `Question ${this.questions.history.length+1}`;
        document.querySelector('.question-query').innerText = this.questions.current.fields.query;
        if (this.questions.current.fields.image?.url)
        {
            document.querySelector('.question-image').style.display = 'block';
            document.querySelector('.question-image').src = this.questions.current.fields.image.url;
        }
        else 
        {
            document.querySelector('.question-image').style.display = 'none';
        }
        document.querySelector('.question-form').onsubmit = (e) => {
            this.socket.send(JSON.stringify({
                type: "answer",
                answer: e.target.answer.value
            })); 
            e.target.answer.value = '';
            document.querySelector('.questions-container').style.display = 'none';
            document.querySelector('.wait-for-question-container').style.display = 'block';

            return false;
        };

        document.querySelector('.wait-for-question-container').style.display = 'none';
        document.querySelector('.questions-container').style.display = 'block';
    }
    wait_for_next_question() {
        document.querySelector('.questions-container').style.display = 'none';
        document.querySelector('.wait-for-question-container').style.display = 'block';
    }
    end_quiz(data) {
        let right_percentage = Math.round(data.rights/data.all*100);
        document.querySelector('.quiz-result-percentage').innerText = `${right_percentage}%`;
        document.querySelector('.quiz-result').innerText = `${data.rights}/${data.all} rights`;
        
        let quiz_end_progress_bar = document.querySelector('.quiz-end-progress-bar');

        let correct = quiz_end_progress_bar.querySelector('.bg-success');
        correct.style.width = `${right_percentage}%`;
        correct.ariaValueNow = right_percentage;

        let incorrect = quiz_end_progress_bar.querySelector('.bg-danger');
        incorrect.style.width = `${100-right_percentage}%`;
        incorrect.ariaValueNow = 100-right_percentage;

        if (data.answers)
        {
            document.querySelector('#show-answers-button').style.display = 'block';
            for (let i in data.answers)
            {
                let question = data.answers[i];
                document.querySelector('.answers-container').innerHTML += `
                <div class="question-container form-group border rounded p-2 ${question.result ? 'correct-answer' : 'incorrect-answer'}">
                    <h3>Question ${parseInt(i)+1}</h3>
                    <div class="form-control">${question.query}</div>
                    ${question.image ? `<img id="question-image-${i}" class="mt-2 w-100 rounded" src="${question.image}">` : ''}
                    <div class="form-control">${question.answer}</div>
                    ${question.correct_answer && !question.result ? `Correct:<div class="form-control correct-answer-2">${question.correct_answer}</div>` : ''}
                </div>
                `;
            }
        }

        document.querySelector('.wait-for-question-container').style.display = 'none';
        document.querySelector('.end-quiz-container').style.display = 'block';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    let sc = new Socket;
});
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
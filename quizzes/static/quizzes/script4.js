class Socket {
    constructor() {
        this.server =  `ws://${window.location.host}/ws/game/${document.querySelector('#game-code').innerText}/`;
        this.socket = new WebSocket(this.server);
        this.init();
        this.participants = {};
        this.quiz = {questions:[]};
    }
    sleep(ms) {
        return new Promise(r => setTimeout(r, ms));
    } 
    init() {
        this.socket.onmessage = async (result) => {
            let data = JSON.parse(result.data);
            switch (data.type)
            {
                case 'new_user':
                    let username = data.username;
                    this.participants[username] = { username, progress: 0, rights: 0 };
                    this.renderParticipants();
                    break;
                case 'remove_user':
                    delete this.participants[data.username];
                    this.renderParticipants();
                    break;
                case "start_game":
                    this.init_game_room();
                    break;
                case "quiz_data":
                    this.quiz = data.data;
                    break;
                case "update_users":
                    for (let [n, v] of Object.entries(data.data))
                    {
                        this.participants[n] = v;
                    }
                    this.renderParticipants();
                    break;
                case "end_game":
                    //await this.sleep(5000);
                    location.href = document.referrer;
                    //window.Location.reload(window.history.go(-1));
                    //window.location.reload(history.back());
                    //location.href = 'http://127.0.0.1:8000/my_quizzes';
                    break;
                case "save_end_game":
                    location.reload();
                    break;
            }
        }
        this.socket.onopen = () => {
            document.addEventListener('change', (e) => {
                let classes = Array.from(e.target.classList);
                if (classes.includes('participant-checkbox'))
                {
                    this.send({ type: 'remove_user', username: e.target.value });
                }
            });
            document.querySelector('.start-button').addEventListener('click', (e) => {
                this.send({ type: 'start_game' });
            });
            document.querySelector('.end-button').addEventListener('click', (e) => {
                $('#messageModal').modal('show');
            });
            document.querySelector('.finish-quiz').addEventListener('click', (e) => {
                this.send({ type: 'end_game' });
            });
            document.querySelector('.save-finish-quiz')?.addEventListener('click', (e) => {
                this.send({ type: 'save_end_game' });
            });
            document.querySelectorAll('.show-answers-for-player-button').forEach(button => 
                button.addEventListener('click', () => {
                    let name = button.dataset.player;
                    let answers_container = document.querySelector(`#answers-of-${name}`);
                    answers_container.style.display = answers_container.style.display == 'block' ? 'none' : 'block';
                    button.innerHTML = answers_container.style.display == 'none' ? `Show <b class="text-info">${name}'s</b> answers` : `Hide <b class="text-info">${name}'s</b> answers`;
                })
            );
        };
    }
    renderParticipants() {
        let participantsDiv = document.querySelector('.participants');
        participantsDiv.innerHTML = '';
        for (let user of Object.values(this.participants))
        {
            participantsDiv.innerHTML += `
                <div class="custom-control custom-checkbox">
                    <input type="checkbox" class="custom-control-input participant-checkbox" id="customCheck-${user.username}" name="users" value="${user.username}" checked>
                    <label class="custom-control-label" for="customCheck-${user.username}">${user.username}</label>
                </div>
            `;
        }
        let container = document.querySelector('.users-progress-container');
        container.innerHTML = '';
        Object.values(this.participants).forEach(user => {
            let result = Math.round(user.rights/user.progress*100);
            container.innerHTML += `
            <div class="row justify-content-between w-100 mt-2">
                <div class="participant-name-admin">${user.username}</div>
                <div class="progress ml-1 mt-1 progress-bar-width">
                    <div class="progress-bar" role="progressbar" style="width: ${user.progress/this.quiz.questions.length*100}%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <div class="text-right w-100">${user.progress}/${this.quiz.questions.length} marked ${isNaN(result) ? 0 : result}% right</div>
            </div>
            `;
        });
    }
    init_game_room() {
        document.querySelector('.wait-participants-room').style.display = 'none';
        document.querySelector('.game-room-admin').style.display = 'block';
    }
    send(data) {
        this.socket.send(JSON.stringify(data));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    let sc = new Socket;
});

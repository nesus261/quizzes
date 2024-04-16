document.addEventListener('DOMContentLoaded', () => {
    // Load image as input file for question 
    (async()=>{
        if (document.querySelector('#add_quiz_form input[name="id"]'))
        {
            for (let question of document.querySelectorAll('.question-container'))
            {
                let image = question.querySelector('img');
                if (image.src)
                {
                    const response = await fetch(image.src);
                    const blob = await response.blob();
                    const file = new File([blob], 'image.png', {
                        type: blob.type,
                        lastModified: new Date(),
                    });
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    question.querySelector('input[type="file"]').files = dataTransfer.files;
                }
            }
        }
    })();
    // show modal if message exist 
    document.querySelector('#add_question').addEventListener('click', addQuestion);
    function addQuestion(e) {
        let container = document.querySelector('#questions-container');
        let id = container.children.length;
        let question = document.createElement('div');
        question.id = `question-container-${id}`;
        question.className = 'question-container form-group border rounded p-2';
        question.innerHTML += `
          <h3>Question ${id+1}</h3>
          <input type="text" name="query-${id}" class="form-control" placeholder="Question" required>
          <img id="question-image-${id}" class="mt-2 w-100 rounded d-none">
          <input type="file" name="image-${id}" id="file-${id}" data-question-id="${id}" hidden>
          <label class="btn btn-light border mt-2" for="file-${id}" accept="image/*">Select image (optional)</label>
          <button class="btn btn-danger remove-question-image d-none" data-question-id="${id}">Remove image</button>
          <input type="text" name="answer-${id}" class="form-control mt-1" placeholder="Expected answer (text or regular expression)" required>
          <button class="btn btn-danger mt-2 remove-question" data-question-id="${id}">Remove question</button>
          <button class="btn btn-light border mt-2 move-up">Move Up</button>
          <button class="btn btn-light border mt-2 move-down">Move Down</button>
        `;
        container.append(question);
        document.querySelector('[name="questions_count"]').value = id+1;
        e.preventDefault();
    }
    document.querySelector('#add_quiz_form').onsubmit = (e) => {
        let fd = new FormData(document.querySelector('#add_quiz_form')); 
        fetch('/add_quiz', {
            method: 'POST',
            body: fd
          })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            if (data.ok)
            {
                location.href = `/quiz/${data.quiz}`;
            }
            else if (data.message)
            {
                $('#messageModal .modal-title')[0].innerText = data.message.title;
                $('#messageModal .modal-body')[0].innerText = data.message.body;
                $('#messageModal').modal('show');
            }
          })
        return false;
    };
    document.addEventListener('click', (e) => {
        let classList = Array.from(e.target.classList);
        if (classList.includes('remove-question-image'))
        {
            let id = e.target.dataset.questionId;
            document.querySelector(`input[name="image-${id}"]`).value = '';
            document.querySelector(`#question-image-${id}`).style.display = 'none';
            e.target.style.display = 'none';
            e.preventDefault();
        }
        else if (classList.includes('remove-question'))
        {
            let id = e.target.dataset.questionId;
            document.querySelector(`#question-container-${id}`).remove();
            fixNumeration();
            e.preventDefault();
        }
        else if (classList.includes('move-up'))
        {
            var container = $(e.target).closest('.question-container');
            container.insertBefore(container.prev());
            fixNumeration();
            e.preventDefault();
        }
        else if (classList.includes('move-down'))
        {
            var container = $(e.target).closest('.question-container');
            container.insertAfter(container.next());
            fixNumeration();
            e.preventDefault();
        }
    });
    document.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0])
        {
            let id = e.target.dataset.questionId;
            let img = document.querySelector(`#question-image-${id}`);
            img.src = URL.createObjectURL(e.target.files[0]);
            img.setAttribute('style', 'display: block !important');
            document.querySelector(`.remove-question-image[data-question-id="${id}"]`).setAttribute('style', 'display: inline-block !important');
        }
    });
    // Fix questions numeration 
    function fixNumeration() {
    $('.question-container').each(function (id) {
        $(this).attr('id', 'question-container-' + id);
        $(this).find('h3').text('Question ' + (id+1));
        $(this).find('[name^="query-"]').attr('name', 'query-' + id);
        $(this).find('[id^="question-image-"]').attr('id', 'question-image-' + id);
        $(this).find('[name^="image-"]').attr('name', 'image-' + id);
        Array.from($(this).find('[data-question-id]')).forEach(el => {
            el.dataset.questionId = id;
        });
        $(this).find('[name^="answer-"]').attr('name', 'answer-' + id);
        $(this).find('[id^="file-"]').attr('id', 'file-' + id);
        $(this).find('[for^="file-"]').attr('for', 'file-' + id);
    });
    }
});
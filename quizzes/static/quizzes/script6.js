document.querySelector('#show-join-quiz-modal').addEventListener('click', () => {
    $('#messageModal3').modal('show');
});
document.querySelector('#join-quiz-form-modal').onsubmit = (e) => {
    let id = document.querySelector('#join-quiz-id').value;
    let fd = new FormData(e.target); 
    fetch(`/check_quiz/${id}`, {
      method: 'POST',
      body: fd
    })
    .then(response => response.json())
    .then(data => {
      if (data.ok)
      {
          location.href = `/game/${id}`;
      }
      else if (data.message)
      {
          $('#messageModal4 .modal-title')[0].innerText = data.message.title;
          $('#messageModal4 .modal-body')[0].innerText = data.message.body;
          $('#messageModal4').modal('show');
      }
    });
    return false;
};
$('#messageModal3').on('shown.bs.modal', function () {
    $('#join-quiz-id').trigger('focus')
})
window.onload = function() {
  for (const btn of document.querySelectorAll('.vote')) {
    btn.addEventListener('click', event => {
      event.preventDefault()
      const id = event.currentTarget.dataset.id;
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      console.log(`Button with id ${id} clicked. Sending POST request...`);

      fetch(`/vote/comment/${id}/true`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
        },
      })
      .then(response => {
        console.log('Received response from server:', response);
        return response.json();
      })
      .then(data => {
        console.log('Received data from server:', data);
        if (data.success) {
          event.currentTarget.classList.toggle('on');
          event.currentTarget.querySelector('.vote-count').textContent = data.new_vote_count;
        } else {
          console.error('Vote failed');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  }
};
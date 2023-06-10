window.addEventListener('load', (event) => {
  console.log('page is fully loaded');
  fetch('/file-list')
    .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log("Received data:", data); // Check what is received from the server
      const fileList = document.getElementById('file-list');
      if (!Array.isArray(data)) {
        console.error("Data is not an array:", data);
        return;
      }
      data.forEach(file => {
        console.log(file);
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.textContent = file;
        tr.appendChild(td);
        fileList.appendChild(tr);
      });
    })
    .catch((error) => {
      console.error('There has been a problem with your fetch operation:', error);
    });
});

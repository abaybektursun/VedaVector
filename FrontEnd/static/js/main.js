window.onload = function() {
    fetch('/file-list')
      .then(response => response.json())
      .then(data => {
        if (data.length > 0) {
          const sourcesSection = document.getElementById('source-options');
          
          // Create and append the "Existing sources" header
          const existingSourcesHeader = document.createElement('h6');
          existingSourcesHeader.className = 'collapse-header';
          existingSourcesHeader.textContent = 'Existing sources:';
          sourcesSection.appendChild(existingSourcesHeader);
  
          // Create and append the "File Source" link
          const fileSourceLink = document.createElement('a');
          fileSourceLink.className = 'collapse-item';
          fileSourceLink.href = 'file_source';
          fileSourceLink.textContent = 'File Source';
          sourcesSection.appendChild(fileSourceLink);
        }
      });
  };
  
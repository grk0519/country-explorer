document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('input[name="country"]');
  if (input) {
    input.addEventListener('focus', () => input.style.borderColor = '#0078d4');
    input.addEventListener('blur', () => input.style.borderColor = '#ccc');
  }

  const mapDiv = document.getElementById('map');
  if (mapDiv) {
    const lat = parseFloat(mapDiv.getAttribute('data-lat'));
    const lng = parseFloat(mapDiv.getAttribute('data-lng'));
    const map = L.map('map').setView([lat, lng], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 18
    }).addTo(map);

    L.marker([lat, lng])
      .addTo(map)
      .bindPopup(`📍 ${mapDiv.dataset.name || 'Selected Country'}`)
      .openPopup();
  }

  const searchInput = document.getElementById('search-input');
  const listContainer = document.getElementById('searchable-list');

  if (searchInput && listContainer) {
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.toLowerCase();
      const items = listContainer.querySelectorAll('li');

      items.forEach(item => {
        item.style.display = item.textContent.toLowerCase().includes(query) ? '' : 'none';
      });
    });
  }
});

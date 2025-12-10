document.addEventListener('DOMContentLoaded', function() {
  loadServices();
  loadContactInfo();
  setupContactForm();
});

function loadServices() {
  fetch('/api/services')
    .then(r => r.json())
    .then(services => {
      const container = document.getElementById('services-container');
      container.innerHTML = services.map(s => `
        <div class="col-md-4 col-lg-4">
          <div class="service-card">
            <div class="service-icon">${s.icon}</div>
            <h5>${s.title}</h5>
            <p>${s.description}</p>
          </div>
        </div>
      `).join('');
    })
    .catch(e => console.error('Error loading services:', e));
}

function loadContactInfo() {
  fetch('/api/contact-info')
    .then(r => r.json())
    .then(info => {
      const container = document.getElementById('contact-info-container');
      container.innerHTML = `
        <div class="contact-info-item">
          <strong>\ud83d\udce7 Email</strong>
          <a href="mailto:${info.email}">${info.email}</a>
        </div>
        <div class="contact-info-item">
          <strong>\ud83d\udcc4 Telefon</strong>
          <a href="tel:${info.phone}">${info.phone}</a>
        </div>
        <div class="contact-info-item">
          <strong>\ud83d\udccd Adres</strong>
          <p>${info.address}</p>
        </div>
        <div class="contact-info-item">
          <strong>\ud83d\udd56 Godziny otwarcia</strong>
          <p>Pn-Pt: ${info.hours.weekday}</p>
          <p>Sob: ${info.hours.saturday}</p>
          <p>Niedz: ${info.hours.sunday}</p>
        </div>
      `;
    })
    .catch(e => console.error('Error loading contact info:', e));
}

function setupContactForm() {
  const form = document.getElementById('contact-form');
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const message = document.getElementById('message').value;
    
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, email, phone, message})
      });
      const data = await response.json();
      showMessage(data.message, data.success);
      if (data.success) form.reset();
    } catch (e) {
      showMessage('B\u0142\u0105d:', false);
    }
  });
}

function showMessage(msg, success) {
  const msgDiv = document.getElementById('form-message');
  msgDiv.className = 'alert ' + (success ? 'alert-success' : 'alert-danger');
  msgDiv.textContent = msg;
  msgDiv.style.display = 'block';
  setTimeout(() => {msgDiv.style.display = 'none';}, 5000);
}

document.getElementById('registrationForm').addEventListener('submit', function(e) {
    const requiredFields = [
        'company_name', 'company_short_name', 'company_phone', 'company_email', 'company_inn',
        'last_name', 'first_name', 'user_phone', 'user_email', 'position', 'password', 'confirm_password'
    ];
    
    let isValid = true;
    
    // Проверка обязательных полей
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Проверка совпадения паролей
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    
    if (password.value !== confirmPassword.value) {
        password.classList.add('is-invalid');
        confirmPassword.classList.add('is-invalid');
        isValid = false;
    }
    
    // Проверка длины пароля
    if (password.value.length < 8) {
        password.classList.add('is-invalid');
        isValid = false;
    }
    
    if (!isValid) {
        e.preventDefault();
        alert('Пожалуйста, заполните все обязательные поля и проверьте правильность ввода пароля');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const positionSelect = document.getElementById('position');
    async function loadPositions() {
        try {
            const response = await fetch(  window.location.origin + '/api/lists/positions');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const positions = await response.json();
			
            
            while (positionSelect.options.length > 1) {
                positionSelect.remove(1);
            }
            
            const groups = {};
            positions.data.forEach(position => {
                if (!groups[position.Group]) {
                    groups[position.Group] = [];
                }
                groups[position.Group].push(position);
            });

            for (const groupName in groups) {
                const optgroup = document.createElement('optgroup');
                optgroup.label = groupName;
                
                groups[groupName].forEach(position => {
                    const option = document.createElement('option');
                    option.value = position.ID;
                    option.textContent = position.Title;
                    optgroup.appendChild(option);
                });
                
                positionSelect.appendChild(optgroup);
            }
            
        } catch (error) {
            console.error('Ошибка при загрузке должностей:', error);
            const errorOption = document.createElement('option');
            errorOption.value = '';
            errorOption.textContent = 'Ошибка загрузки должностей';
            positionSelect.appendChild(errorOption);
        }
    }
    
    loadPositions();
});

/*
    if (grecaptcha.getResponse().length === 0) {
        e.preventDefault();
        document.getElementById('recaptcha-error').classList.remove('d-none');
        document.querySelector('.g-recaptcha').style.border = '1px solid #dc3545';
        document.querySelector('.g-recaptcha').style.borderRadius = '4px';
        document.querySelector('.g-recaptcha').style.padding = '2px';
        
        window.scrollTo({
            top: document.querySelector('.g-recaptcha').offsetTop - 100,
            behavior: 'smooth'
        });
        
        return false;
    }
    
    return true;
});

// Убираем ошибку при взаимодействии с капчей
grecaptcha.ready(function() {
    grecaptcha.execute();
});*/
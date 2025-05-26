// Script para logout melhorado
function confirmLogout() {
    if (confirm('Deseja realmente sair do sistema?')) {
        // Criar formulário para POST
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/logout/';
        
        // Adicionar CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);
        
        // Adicionar ao body e submeter
        document.body.appendChild(form);
        form.submit();
    }
    return false;
}

// Fazer logout automático após inatividade (opcional)
let inactivityTimer;
function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    // 30 minutos de inatividade
    inactivityTimer = setTimeout(function() {
        if (confirm('Você ficou inativo por muito tempo. Deseja continuar logado?')) {
            resetInactivityTimer();
        } else {
            window.location.href = '/logout/';
        }
    }, 30 * 60 * 1000); // 30 minutos
}

// Resetar timer em qualquer atividade
document.addEventListener('mousemove', resetInactivityTimer);
document.addEventListener('keypress', resetInactivityTimer);
document.addEventListener('click', resetInactivityTimer);

// Iniciar timer quando página carrega
if (document.querySelector('.navbar-nav .dropdown')) {
    resetInactivityTimer();
}

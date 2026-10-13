/* ═══════════════════════════════════════════════════════
   SecureBank — Client Application Logic
   ═══════════════════════════════════════════════════════ */

// ─── Toast Notifications ───
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let iconClass = 'fa-solid fa-circle-info';
    if (type === 'success') iconClass = 'fa-solid fa-circle-check';
    if (type === 'error') iconClass = 'fa-solid fa-circle-exclamation';

    toast.innerHTML = `
        <i class="${iconClass} toast-icon"></i>
        <div class="toast-message">${escapeHtml(message)}</div>
        <button class="toast-close" onclick="dismissToast(this.parentElement)">
            <i class="fa-solid fa-xmark"></i>
        </button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        dismissToast(toast);
    }, 4500);
}

function dismissToast(toast) {
    if (!toast || toast.classList.contains('fade-out')) return;
    toast.classList.add('fade-out');
    setTimeout(() => {
        if (toast.parentElement) toast.remove();
    }, 300);
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, function (m) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[m];
    });
}

// ─── Modal Management ───
function openModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.add('active');
    const firstInput = modal.querySelector('input');
    if (firstInput) setTimeout(() => firstInput.focus(), 100);
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.remove('active');
}

// Close modals when clicking backdrop or pressing ESC
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
        const overlay = document.getElementById('transferSuccessOverlay');
        if (overlay) overlay.classList.remove('active');
    }
});

// ─── Mobile Sidebar Navigation ───
document.addEventListener('DOMContentLoaded', () => {
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (mobileBtn && sidebar && overlay) {
        mobileBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('active');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }

    // Secure Logout Button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                const res = await fetch('/api/logout', { method: 'POST' });
                const data = await res.json();
                if (data.success) {
                    showToast('Logged out securely.', 'info');
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 400);
                }
            } catch (err) {
                window.location.href = '/login';
            }
        });
    }
});

// ─── Modal Deposit Action ───
async function handleDeposit(e) {
    e.preventDefault();
    const input = document.getElementById('depositAmount');
    const amount = parseFloat(input.value);
    const btn = document.getElementById('depositSubmitBtn');

    if (isNaN(amount) || amount <= 0) {
        showToast('Please enter a valid deposit amount greater than ₹0.00', 'error');
        return;
    }

    btn.disabled = true;

    try {
        const res = await fetch('/api/deposit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount })
        });
        const data = await res.json();

        if (data.success) {
            showToast(data.message, 'success');
            closeModal('depositModal');
            input.value = '';

            // Update balance on screen if available
            const balDisplay = document.getElementById('balanceAmountDisplay');
            if (balDisplay) {
                balDisplay.textContent = '₹ ' + data.balance.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            }
            // Auto reload after brief delay to refresh transactions
            setTimeout(() => window.location.reload(), 900);
        } else {
            showToast(data.message || 'Deposit failed.', 'error');
        }
    } catch (err) {
        showToast('Network error during deposit.', 'error');
    } finally {
        btn.disabled = false;
    }
}

// ─── Modal Withdraw Action ───
async function handleWithdraw(e) {
    e.preventDefault();
    const input = document.getElementById('withdrawAmount');
    const amount = parseFloat(input.value);
    const btn = document.getElementById('withdrawSubmitBtn');

    if (isNaN(amount) || amount <= 0) {
        showToast('Please enter a valid withdrawal amount greater than ₹0.00', 'error');
        return;
    }

    btn.disabled = true;

    try {
        const res = await fetch('/api/withdraw', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount })
        });
        const data = await res.json();

        if (data.success) {
            showToast(data.message, 'success');
            closeModal('withdrawModal');
            input.value = '';

            // Update balance on screen if available
            const balDisplay = document.getElementById('balanceAmountDisplay');
            if (balDisplay) {
                balDisplay.textContent = '₹ ' + data.balance.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            }
            // Auto reload after brief delay to refresh transactions
            setTimeout(() => window.location.reload(), 900);
        } else {
            showToast(data.message || 'Withdrawal failed. Check balance.', 'error');
        }
    } catch (err) {
        showToast('Network error during withdrawal.', 'error');
    } finally {
        btn.disabled = false;
    }
}

// Simple markdown renderer
function renderMarkdown(text) {
    if (!text) return '';
    let html = text
        // Escape HTML first
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        // Headings
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        // Bold / italic
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        // Inline code
        .replace(/`(.+?)`/g, '<code>$1</code>')
        // Blockquote
        .replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>')
        // Unordered list items
        .replace(/^[-*] (.+)$/gm, '<li>$1</li>')
        // Wrap consecutive li in ul
        .replace(/(<li>.*<\/li>\n?)+/gs, m => `<ul>${m}</ul>`)
        // Paragraphs (double newline)
        .split(/\n\n+/)
        .map(block => {
            block = block.trim();
            if (!block) return '';
            if (block.match(/^<(h[1-6]|ul|ol|blockquote)/)) return block;
            return `<p>${block.replace(/\n/g, '<br>')}</p>`;
        })
        .join('\n');
    return html;
}

// Render entry body if present
const entryBody = document.getElementById('entry-body');
if (entryBody) {
    entryBody.innerHTML = renderMarkdown(entryBody.textContent);
}

// Build mobile nav dynamically
const sections = [
    {id: 'zoning', icon: '⚖️', label: 'Zoning'},
    {id: 'legislation', icon: '📜', label: 'Laws'},
    {id: 'portsmouth', icon: '🏛️', label: 'Portsmouth'},
    {id: 'people', icon: '👥', label: 'People'},
    {id: 'meetings', icon: '📝', label: 'Meetings'},
    {id: 'glossary', icon: '📖', label: 'Glossary'},
];

const mobileNav = document.createElement('nav');
mobileNav.className = 'mobile-nav';
const currentPath = window.location.pathname;

sections.forEach(s => {
    const a = document.createElement('a');
    a.href = `/section/${s.id}`;
    a.className = 'mobile-nav-link' + (currentPath.includes(s.id) ? ' active' : '');
    a.innerHTML = `<span class="mobile-nav-icon">${s.icon}</span>${s.label}`;
    mobileNav.appendChild(a);
});

document.body.appendChild(mobileNav);

// Service Worker registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(() => console.log('SW registered'))
            .catch(e => console.log('SW failed:', e));
    });
}

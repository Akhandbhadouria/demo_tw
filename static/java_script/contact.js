const expandButton = document.getElementById('expandButton');
const contactContent = document.getElementById('contactContent');
const overlay = document.getElementById('overlay');
const toast = document.getElementById('success-toast');

let isExpanded = false;

expandButton.addEventListener('click', function () {
    if (isExpanded) {
        contactContent.classList.add('collapsed');
        overlay.classList.remove('hidden');
        expandButton.classList.remove('expanded');
    } else {
        contactContent.classList.remove('collapsed');
        overlay.classList.add('hidden');
        expandButton.classList.add('expanded');
    }

    isExpanded = !isExpanded;
});

if (window.innerWidth <= 768) {
    setTimeout(() => {
        if (!isExpanded) {
            contactContent.classList.remove('collapsed');
            overlay.classList.add('hidden');
            expandButton.classList.add('expanded');
            isExpanded = true;
        }
    }, 2000);
}

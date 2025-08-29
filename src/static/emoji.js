class EmojiPicker extends HTMLElement {
    constructor() {
        super();
        this.innerHTML = `
            <div class="emoji-picker-container">
                <div class="emoji-picker">
                    <div class="emoji-category">
                        <span>Часто используемые</span>
                        <div class="emoji-grid">
                            <span class="emoji">😀</span><span class="emoji">😂</span><span class="emoji">😍</span>
                            <span class="emoji">😊</span><span class="emoji">🥰</span><span class="emoji">😎</span>
                            <span class="emoji">🙏</span><span class="emoji">👍</span><span class="emoji">❤️</span>
                            <span class="emoji">🔥</span>
                        </div>
                    </div>
                    <div class="emoji-category">
                        <span>Смайлики</span>
                        <div class="emoji-grid">
                            <span class="emoji">😀</span><span class="emoji">😃</span><span class="emoji">😄</span>
                            <span class="emoji">😁</span><span class="emoji">😆</span><span class="emoji">😅</span>
                            <span class="emoji">😂</span><span class="emoji">🤣</span><span class="emoji">😊</span>
                            <span class="emoji">😇</span><span class="emoji">🙂</span><span class="emoji">🙃</span>
                            <span class="emoji">😉</span><span class="emoji">😌</span><span class="emoji">😍</span>
                            <span class="emoji">🥰</span><span class="emoji">😘</span><span class="emoji">😗</span>
                            <span class="emoji">🙏</span><span class="emoji">🔥</span><span class="emoji">👍</span>
                            <span class="emoji">❤️</span><span class="emoji">😎</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
}

customElements.define('emoji-picker', EmojiPicker);

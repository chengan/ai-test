function addMessage(content, type) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // 显示用户消息
    addMessage(message, 'user');
    input.value = '';
    
    // 创建AI消息占位
    const aiMessageDiv = document.createElement('div');
    aiMessageDiv.className = 'message ai-message';
    document.getElementById('chatMessages').appendChild(aiMessageDiv);
    
    // 发送请求到后端
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        function readStream() {
            reader.read().then(({done, value}) => {
                if (done) return;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');
                
                lines.forEach(line => {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            if (data.status === 'success') {
                                aiMessageDiv.textContent += data.content;
                                aiMessageDiv.scrollIntoView({ behavior: 'smooth' });
                            }
                        } catch (e) {
                            console.error('解析响应失败:', e);
                        }
                    }
                });
                
                readStream();
            }).catch(error => {
                aiMessageDiv.textContent = '发生错误，请重试';
                console.error('读取响应失败:', error);
            });
        }
        
        readStream();
    }).catch(error => {
        aiMessageDiv.textContent = '连接失败，请重试';
        console.error('请求失败:', error);
    });
} 
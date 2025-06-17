const token = '8053105701:AAEifBvwv6q7Y3QEF873hMn49A9eA9PO1Xo';

async function fetchMessages() {
    try {
        const response = await fetch(`https://api.telegram.org/bot${token}/getUpdates`);
        const data = await response.json();
        handleResponse(data);
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('message').textContent = 'Ошибка загрузки данных';
    }
}

function handleResponse(response) {
    console.log('Ответ API:', response);

    if (response.ok && response.result?.length > 0) {
        const lastUpdate = response.result[response.result.length - 1];
        const message = lastUpdate.message ?? lastUpdate.edited_message;
        const user = message?.from;
        
        if (!user) {
            document.getElementById('message').textContent = 'Нет данных об отправителе';
            return;
        }

        const username = user.username || [user.first_name, user.last_name].filter(Boolean).join(' ') || 'Аноним';
        document.getElementById('username').textContent = `@${username}`;
        document.getElementById('message').textContent = message.text || 'Сообщение без текста';
        fetchUserPhoto(user.id);
    } else {
        document.getElementById('message').textContent = 'Нет сообщений';
    }
}

async function fetchUserPhoto(userId) {
    try {
        const response = await fetch(`https://api.telegram.org/bot${token}/getUserProfilePhotos?user_id=${userId}`);
        const data = await response.json();
        
        if (data.ok && data.result.photos?.length > 0) {
            const fileId = data.result.photos[0][0].file_id;
            
            // Получаем полный путь к файлу
            const fileResponse = await fetch(`https://api.telegram.org/bot${token}/getFile?file_id=${fileId}`);
            const fileData = await fileResponse.json();
            
            if (fileData.ok) {
                const photoUrl = `https://api.telegram.org/file/bot${token}/${fileData.result.file_path}`;
                const avatarBlock = document.getElementById('avatar');
                avatarBlock.innerHTML = `<img src="${photoUrl}" alt="Аватар">`;
            }
        } else {
            document.getElementById('avatar').innerHTML = '<div class="no-avatar"></div>';
        }
    } catch (error) {
        console.error('Ошибка загрузки аватара:', error);
    }
}

window.onload = function() {
    fetchMessages();   
    document.getElementById('refresh-button').addEventListener('click', fetchMessages);         
};


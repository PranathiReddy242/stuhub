document.addEventListener('DOMContentLoaded', () => {
    const postBtn = document.getElementById('post-btn');
    const postContent = document.getElementById('post-content');
    const feed = document.getElementById('feed');

    if (postBtn && postContent) {
        postBtn.addEventListener('click', async () => {
            if (postContent.value.trim()) {
                try {
                    const response = await fetch('/api/posts', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            content: postContent.value
                        })
                    });

                    if (response.ok) {
                        postContent.value = '';
                        loadPosts();
                    }
                } catch (error) {
                    console.error('Error posting:', error);
                }
            }
        });
    }

    async function loadPosts() {
        if (!feed) return;
        
        try {
            const response = await fetch('/api/posts');
            const posts = await response.json();
            
            feed.innerHTML = posts.map(post => `
                <div class="post">
                    <div class="post-header">
                        ${post.username ? 
                            `<strong>${post.username}</strong>` : 
                            '<em>Anonymous</em>'
                        }
                        <small>${new Date(post.created_at).toLocaleString()}</small>
                    </div>
                    <p>${post.content}</p>
                    <div class="post-actions">
                        <button class="like-btn" data-id="${post.id}">
                            ❤️ ${post.likes}
                        </button>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading posts:', error);
        }
    }

    loadPosts();
});
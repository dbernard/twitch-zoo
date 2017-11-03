(function(Console, Document, Timer) {
    function fetchJSON(url) {
        const headers = new Headers({
            'Content-Type': 'text/plain' // Needs to be plain for CORS-permissivity
        });
        const init = {
            headers,
            mode: 'cors'
        };
        return fetch(new Request(url, init));
    }

    class UserStatsService {
        constructor() {
            this.currentStats = {};
        }

        loadData() {
            return fetchJSON('/streamers').then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    Console.error('Bad response!');
                    throw 'Bad response!';
                }
            }).then((stats) => {
                for (const user of stats) {
                    this.currentStats[user.username] = user;
                }
            });
        }

        renderElement(element, info) {
            for (const field of ['viewers', 'fps', 'views']) {
                element.querySelector(`.stats .${field} > span`).innerText = info[field];
            }
        }

        render() {
            for (const stream of Document.querySelectorAll('.stream')) {
                const username = stream.dataset.twitchUsername;
                const streamInfo = this.currentStats[username];
                if (streamInfo !== undefined) {
                    this.renderElement(stream, streamInfo);
                }
            }
        }

        start() {
            return this.loadData()
                .then(() => this.render())
                .then(() => this.timer = Timer.setInterval(() => this.loadData().then(() => this.render()), 30000));
        }

        stop() {
            if (this.timer) {
                Timer.clearInterval(this.timer);
            }
        }
    }
    const statsService = new UserStatsService();
    statsService.start();
})(console, document, window);

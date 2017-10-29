(function(Console, Document, Timer, TEAM_ID) {
    const TEAM_URL = 'https://www.extra-life.org/index.cfm?fuseaction=donorDrive.team&format=json&teamID=';

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

    class TeamProgressBar {
        constructor(team_id) {
            this.team_id = team_id;
            this.min = 0;
            this.max = 0;
            this.current = 0;
            this.label = 'Loading team progress...';
            this.render();
        }

        loadData() {
            return fetchJSON(`${TEAM_URL}${this.team_id}`).then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    Console.error('Bad response!');
                    throw 'Bad response!';
                }
            }).then((stats) => {
                this.max = stats.fundraisingGoal;
                this.current = stats.totalRaisedAmount;
                this.label = `$${this.current}`;
            });
        }

        render() {
            const progress = Document.querySelector('#teamProgress > .progress-bar');
            progress.setAttribute('aria-valuemax', this.max);
            progress.setAttribute('aria-valuenow', this.current);
            progress.style.minWidth = `${100 * this.current / (this.max || 1)}%`;
            progress.innerText = this.label;
        }

        start() {
            return this.loadData()
                .then(() => this.render())
                .then(() => this.timer = Timer.setInterval(() => this.loadData().then(() => this.render()), 10000));
        }

        stop() {
            if (this.timer) {
                Timer.clearInterval(this.timer);
            }
        }
    }
    const teamProgress = new TeamProgressBar(TEAM_ID);
    teamProgress.start();
})(console, document, window, window.TEAM_ID);

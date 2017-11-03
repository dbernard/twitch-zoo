(function(Console, Document, Timer) {
    const TEAM_URL = 'https://www.extra-life.org/index.cfm?fuseaction=donorDrive.team&format=json&teamID=';
    const INDIVIDUAL_URL = 'https://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&format=json&participantID=';

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

    function getFundraisingId(element) {
        const fundraisingId = element.dataset.fundraisingId;
        if (fundraisingId === undefined) {
            throw 'Fundraising ID not found!';
        }
        return fundraisingId;
    }

    class FundraisingProgressBar {
        constructor(progressElement, endpoint) {
            this.endpoint = endpoint;
            this.min = 0;
            this.max = 0;
            this.current = 0;
            this.label = 'Loading team progress...';
            this.progressElement = progressElement;
            this.render();
        }

        loadData() {
            return fetchJSON(this.endpoint).then((response) => {
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
            this.progressElement.setAttribute('aria-valuemax', this.max);
            this.progressElement.setAttribute('aria-valuenow', this.current);
            this.progressElement.style.minWidth = `${100 * this.current / (this.max || 1)}%`;
            this.progressElement.innerText = this.label;
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
    const teamProgressElement = Document.querySelector('#teamProgress > .progress-bar');
    const teamProgress = new FundraisingProgressBar(teamProgressElement,
                                                    `${TEAM_URL}${getFundraisingId(teamProgressElement)}`);
    teamProgress.start();
    for (const individualProgressElement of Document.querySelectorAll('.individual-progress > .progress-bar')) {
        const individualProgress = new FundraisingProgressBar(individualProgressElement,
            `${INDIVIDUAL_URL}${getFundraisingId(individualProgressElement)}`);
        individualProgress.start();
    }
})(console, document, window);

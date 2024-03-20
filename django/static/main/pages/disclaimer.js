function renderDisclaimerPage() {
    document.getElementById('app').innerHTML = `
        <div class="all-screen">
            <div class="disclaimer">

                <div class="disclaimer-container-img">
                    <img class="disclaimer-img" src="/static/main/img/loading.gif" class="logo">
				</div>
					
				<div class="disclaimer-content">

					<h2>Transcendence - Final Testing Phase</h2>
					
					</br>
					<p>We are currently in the final testing phase for our Transcendence.</p>
					<p>If you encounter any bugs, <u>we encourage you to send us a message on Discord</u> ( <i>lpupier</i> ).</p>
					<p>Please note that we are primarily interested in issues that affect the functionality of the website. Minor CSS issues are not our priority.</p>
					<p>The mobile version does not work with the pong game, please use a computer.</p>
					<p>Thank you for your understanding and support!</p>
					
					</br>
					<p><i>lpupier & tgiraudo & ezanotti</i></p>

					</br>
					<button data-route="/pong/">I understand →</button>

				</div>
            </div>
        </div>
    `;
}
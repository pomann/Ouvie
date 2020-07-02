import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'hello';
  landingPage = true;
  loginSignup = false;
  showLogin = false;
  showSignup = false;

  toggleLS($event) {
    this.landingPage = !this.landingPage;
    this.loginSignup = !this.loginSignup;

    if ($event === 'login') {
      this.showLogin = true;
    } else {
      this.showSignup = true;
    }
  }
}

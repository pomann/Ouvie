import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { SharedService } from '../shared.service';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
  userActivity;
  userInactive: Subject<any> = new Subject();

  username: string;
  email: string;
  activeProject: string;

  showProjects = true;
  showProjectDetails = false;
  showUserDetails = false;

  constructor(private sharedService: SharedService, private router: Router) {
    this.setTimeout();
   }

  ngOnInit() {
    this.sharedService.getUsername.subscribe(username => this.username = username);
    this.sharedService.getEmail.subscribe(email => this.email = email);

    if (!this.username) {
      this.router.navigate(['/login']);
    }

    this.userInactive.subscribe(() => {
      this.router.navigate(['/login']);
    });
  }

  displayProjects(isProject = true) {
    this.showProjects = isProject;
    this.showProjectDetails = !isProject;
  }

  toggleUserDetails() {
    this.showUserDetails = !this.showUserDetails;
  }

  setProjectName(projectName: string) {
    this.activeProject = projectName;
    this.displayProjects(false);
  }

  logout(bool: boolean) {
    if (bool === true) {
      this.router.navigate(['/login']);
    }
  }

  setTimeout() {
    this.userActivity = setTimeout(() => {
      this.userInactive.next(null);
    }, 30000);
  }

  @HostListener('window:mousemove')
  refreshUserState() {
    this.resetInactiveCounter();
  }

  @HostListener('window:keydown', ['$event'])
  handleKeyDown(event: KeyboardEvent) {
    this.resetInactiveCounter();
  }

  resetInactiveCounter() {
    clearTimeout(this.userActivity);
    this.setTimeout();
  }

  ngOnDestroy(): void {
    // Called once, before the instance is destroyed.
    // Add 'implements OnDestroy' to the class.
    this.sharedService.setUsername('');
    this.sharedService.setEmail('');
    window.localStorage.removeItem('Token');
  }
}

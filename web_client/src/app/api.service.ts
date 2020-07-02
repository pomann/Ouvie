import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

const remoteUrl = 'http://127.0.0.1:5000/api/v1/';
const localUrl = 'assets/api/v1/';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  getUsernameAvailability(name: string) {
    return this.http.get(remoteUrl + 'auth/register/user?' + 'user=' + name);
  }

  getEmailAvailability(email: string) {
    return this.http.get(remoteUrl + 'auth/register/email?' + 'email=' + email);
  }

  getUserAuth(user: string, pswd: string) {
    return this.http.get(remoteUrl + 'auth/login?' + 'user=' + user + '&password=' + pswd);
  }

  getRegisterAuth(name: string, user: string, email: string, pswd: string, optin: boolean) {
    return this.http.get(remoteUrl + 'auth/register/verify?' + 'name=' + name
                                                   + '&user=' + user
                                                   + '&email=' + email
                                                   + '&pswd=' + pswd
                                                   + '&optin=' + optin);
  }

  getUserProjects(username: string) {
    const headers = new HttpHeaders().set('Authorization', `${window.localStorage.getItem('Token')}`);

    return this.http.get(remoteUrl + 'retrieve/project?' + 'user=' + username, {headers});
  }

  getProjectDetails(projectName: string, username: string, branch = 'master') {
    const headers = new HttpHeaders().set('Authorization', `${window.localStorage.getItem('Token')}`);

    return this.http.get(remoteUrl + 'retrieve/commit/files?' + 'user=' + username +
    '&pname=' + projectName + '&branch=' + branch, {headers});
  }

  getUserFullDetails(username: string) {
    const headers = new HttpHeaders().set('Authorization', `${window.localStorage.getItem('Token')}`);

    return this.http.get(remoteUrl + 'retrieve/user/details?' + 'user=' + username, {headers});
  }

  getProjectCommitCount(pname: string, username: string, branch = '') {
    const headers = new HttpHeaders().set('Authorization', `${window.localStorage.getItem('Token')}`);

    return this.http.get(remoteUrl + 'retrieve/commit/count?' + 'user=' + username + '&pname=' + pname + '&branch=' + branch, {headers});
  }

  getProjectBranchCount(username: string, pname: string) {
    const headers = new HttpHeaders().set('Authorization', `${window.localStorage.getItem('Token')}`);

    return this.http.get(remoteUrl + 'retrieve/branch/count?' + 'user=' + username + '&pname=' + pname, {headers});
  }
}

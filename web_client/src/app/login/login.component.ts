import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Responses } from '../responses';
import { ApiService } from '../api.service';
import { SharedService } from '../shared.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  rsp: boolean;
  isInvalid = false;

  constructor(private formBuilder: FormBuilder, private api: ApiService, private router: Router, private sharedService: SharedService) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
  });
  }

  get f() { return this.loginForm.controls; }

  async onSubmit() {
      this.getFormAuth(this.f.username.value, this.f.password.value);
  }

  getFormAuth(user: string, pswd: string) {
    if (user !== '' && pswd !== '') {
      this.api.getUserAuth(user, pswd)
        .subscribe((data: Responses) => {
              (data.code === 'OV1111') ? this.rsp = true : this.rsp = false;
              window.localStorage.setItem('Token', data.data[1]);
              this.userAuth(user, data.data[0]);
            });
    }
  }

  userAuth(user: string, email: string) {
    if (this.rsp) {
      this.isInvalid = false;
      this.sharedService.setUsername(user);
      this.sharedService.setEmail(email);
      this.router.navigate(['/dashboard']);
    } else {
      this.isInvalid = true;
    }
  }

}

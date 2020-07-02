import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ApiService } from '../api.service';
import { Responses } from '../responses';

@Component({
  selector: 'app-user-details',
  templateUrl: './user-details.component.html',
  styleUrls: ['./user-details.component.scss']
})
export class UserDetailsComponent implements OnInit {

  @Input() username: string;
  @Input() email: string;
  @Output() isLoggedOut = new EventEmitter<boolean>();

  fullName: string;

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.api.getUserFullDetails(this.username)
        .subscribe((data: Responses) => {
              if (data.code === 'OV1111') {
                this.fullName = data.data;
              }
            });
  }

  logout() {
    this.isLoggedOut.emit(true);
  }

}

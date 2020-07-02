import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ApiService } from '../api.service';
import { Responses } from '../responses';

@Component({
  selector: 'app-dashboard-projects',
  templateUrl: './dashboard-projects.component.html',
  styleUrls: ['./dashboard-projects.component.scss']
})
export class DashboardProjectsComponent implements OnInit {

  @Output() projectName = new EventEmitter<string>();
  @Input() username: string;
  projects: [string];

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.api.getUserProjects(this.username)
        .subscribe((data: Responses) => {
              console.log(data);
              if (data.code === 'OV1111') {
                this.projects = data.data;
              }
            });
  }

  displayProject(project: string) {
    this.projectName.emit(project);
  }

}

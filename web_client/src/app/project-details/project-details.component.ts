import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ApiService } from '../api.service';
import { Responses } from '../responses';

@Component({
  selector: 'app-project-details',
  templateUrl: './project-details.component.html',
  styleUrls: ['./project-details.component.scss']
})
export class ProjectDetailsComponent implements OnInit {

  @Input() username: string;
  @Input() projectName: string;
  @Output() showProjects = new EventEmitter<boolean>();

  files: [string];
  commitCount: string;
  commitsOnBranch: string;
  lastCommit = '';
  activeBranch = 'master';
  branches = ['master'];

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.api.getProjectDetails(this.projectName, this.username)
        .subscribe((data: Responses) => {
              if (data.code === 'OV1111') {
                this.files = data.data;
              }
            });

    this.api.getProjectCommitCount(this.projectName, this.username)
        .subscribe((data: Responses) => {
              console.log(data);
              if (data.code === 'OV1111') {
                this.commitCount = data.data[0];
              }
            });

    this.api.getProjectCommitCount(this.projectName, this.username, this.activeBranch)
        .subscribe((data: Responses) => {
              console.log(data);
              if (data.code === 'OV1111') {
                this.commitsOnBranch = data.data.length;
                this.lastCommit = data.data[data.data.length - 1];
              }
            });

    this.api.getProjectBranchCount(this.projectName, this.username)
            .subscribe((data: Responses) => {
                  if (data.code === 'OV1111') {
                    this.branches = data.data;
                  }
                });
  }

  displayProjects() {
    this.showProjects.emit(true);
  }
  onBranchChange(e: any) {
    this.activeBranch = e.target.value;

    this.api.getProjectDetails(this.projectName, this.username, this.activeBranch)
        .subscribe((data: Responses) => {
              if (data.code === 'OV1111') {
                this.files = data.data;
              }
            });

    this.api.getProjectCommitCount(this.projectName, this.username, this.activeBranch)
        .subscribe((data: Responses) => {
              if (data.code === 'OV1111') {
                this.commitsOnBranch = data.data.length;
                this.lastCommit = data.data[data.data.length - 1];
              }
            });
  }

}

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProjectList } from './project-list/project-list.component';

const routes: Routes = [
  { path: 'search', component: ProjectList },
//   { path: 'adduser', component: UserFormComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

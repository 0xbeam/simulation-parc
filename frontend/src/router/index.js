import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ProjectList from '../views/ProjectList.vue'
import Process from '../views/MainView.vue'
import SimulationView from '../views/SimulationView.vue'
import SimulationRunView from '../views/SimulationRunView.vue'
import ReportView from '../views/ReportView.vue'
import InteractionView from '../views/InteractionView.vue'
import Login from '../views/Login.vue'
import AppShell from '../components/layout/AppShell.vue'
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  // New dashboard route
  {
    path: '/',
    name: 'Dashboard',
    component: ProjectList
  },
  // Home / upload page (accessible directly)
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  // New project routes wrapped in AppShell
  {
    path: '/project/:id',
    component: AppShell,
    children: [
      {
        path: '',
        name: 'ProjectMain',
        component: Process,
        props: route => ({ projectId: route.params.id })
      },
      {
        path: 'simulate',
        name: 'ProjectSimulation',
        component: SimulationView,
        props: route => ({ simulationId: route.params.id })
      },
      {
        path: 'run',
        name: 'ProjectRun',
        component: SimulationRunView,
        props: route => ({ simulationId: route.params.id })
      },
      {
        path: 'report',
        name: 'ProjectReport',
        component: ReportView,
        props: route => ({ reportId: route.params.id })
      },
      {
        path: 'explore',
        name: 'ProjectExplore',
        component: InteractionView,
        props: route => ({ reportId: route.params.id })
      }
    ]
  },
  // Legacy routes (keep old flow working)
  {
    path: '/process/:projectId',
    name: 'Process',
    component: Process,
    props: true
  },
  {
    path: '/simulation/:simulationId',
    name: 'Simulation',
    component: SimulationView,
    props: true
  },
  {
    path: '/simulation/:simulationId/start',
    name: 'SimulationRun',
    component: SimulationRunView,
    props: true
  },
  {
    path: '/report/:reportId',
    name: 'Report',
    component: ReportView,
    props: true
  },
  {
    path: '/interaction/:reportId',
    name: 'Interaction',
    component: InteractionView,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

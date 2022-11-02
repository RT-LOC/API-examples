const axios = require('axios')
const qs = require("qs")

const http = axios.create({
  baseURL: 'https://api.cloud.rtloc.com',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
    // Authorization: 'Bearer {token}'
  }
})


const login = async (user) => {
  let resp
  resp = await http.post("/auth/login",
    qs.stringify(user)
  )
  return resp.data
}

const getProjects = async token => {
  let resp
  resp = await http.get("/project", {
    headers: { Authorization: "Bearer " + token }
  });
  return resp.data
}

const getClients = async token => {
  let resp
  resp = await http.get("/client", {
    headers: { Authorization: "Bearer " + token }
  });
  return resp.data
}

const getClient = async (token, clientId) => {
  let resp
  resp = await http.get(`/client/${clientId}`, {
    headers: { Authorization: "Bearer " + token }
  });
  return resp.data
}

const getUsers = async token => {
  let resp
  resp = await http.get("/user", {
    headers: { Authorization: "Bearer " + token }
  });
  return resp.data
}

const demo = async user => {
  const { token } = await login(user)

  const projects = await getProjects(token)
  console.log("--- Projects:")
  console.log(projects)

  const clients = await getClients(token)
  console.log("--- Clients:")
  console.log(clients)

  const clientId = "3c7471f1180213232c5a1231"
  const client = await getClient(token, clientId)
  console.log(`--- Client id = "${clientId}":`)
  console.log(client)

  const users = await getUsers(token)
  console.log("--- Users:")
  console.log(users)
}

const user ={ email: 'demo@rtloc.com', password: '12345'}
demo(user)
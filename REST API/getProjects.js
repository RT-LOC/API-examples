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

const demo = async user => {
  const { token } = await login(user)
  const projects = await getProjects(token)
  console.log(projects)
}

const user ={ email: 'demo@rtloc.com', password: '12345'}
demo(user)
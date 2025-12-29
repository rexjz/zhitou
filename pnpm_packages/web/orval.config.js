import { defineConfig } from "orval";

export default defineConfig({
  zhitou: {
    input: {
      target: "http://localhost:6008/openapi.json",
    },
    output: {
      mode: "tags-split",                 
      target: "src/sdk",                   
      client: "swr",                       
      schemas: "src/sdk/models",           
      mock: false,
    },
  },
});

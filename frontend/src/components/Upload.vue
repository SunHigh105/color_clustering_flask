<template>
  <div>
    <div class="loading" v-show="loading">
      <div class="loading__inner">
        <h3>Uploading...</h3>
        <img src="@/assets/icon_loader_f_ww_01_s1.gif">
      </div>
    </div>
    <div class="file-upload">
      <form method="post" enctype="multipart/form-data">
        <div class="file-upload__row">
          <p>1. Select image</p>
          <label for="file">Select image
            <input @change="selectedFile" type="file" name="file" id="file">
          </label>   
        </div>
        <div class="file-upload__row">
          <p>2. Select cluster</p>
          <select v-model="cluster" name="cluster">
            <option>Select cluster</option>
            <option v-for="n in 5" v-bind:key="n.index" v-bind:value="n">{{ n }}</option>
          </select>
        </div> 
        <div class="file-upload__row">
          <p>3. Upload & Clustering</p>
          <button @click="upload" type="button">Upload</button>
        </div>
      </form>
      <div class="file-upload__prev">
        <img
          v-show="uploadFile"
          :src="uploadFile"
          alt=""
        />
      </div>
    </div>
    <div class="color-bar">
      <div 
        v-for="row in colorList" 
        v-bind:key="row.index" 
        v-bind:style="'background-color: rgb(' + row['color_list'][0] + ',' + row['color_list'][1] + ',' + row['color_list'][2] + '); width:' + row['histogram'] + '%;'"
      ></div>
    </div>
    <div class="color-info">
      <p v-for="row in colorList"
        v-bind:key="row.index">
        <pre>【{{ row['cluster'] }}】R:{{ row['color_list'][0] }}  G:{{ row['color_list'][1] }}  B:{{ row['color_list'][2] }}</pre>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      uploadFile: null,
      fileName: '',
      fileType: '',
      cluster: 1,
      loading: false,
      colorList: [],
    }
  },
  methods: {
    selectedFile (e) {
      let files = e.target.files
      this.createImage(files[0])
      this.uploadFile = files[0]
      this.fileName = files[0].name
      this.fileType = files[0].type
    },
    upload () {
      let params = new FormData()
      params.append('file', this.uploadFile)
      params.append('filename', this.fileName)
      params.append('filetype', this.fileName)
      params.append('cluster', this.cluster)
      this.loading = true
      axios.post('/uploads', params, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          this.loading = false
          alert('File Upload Success!')
          this.colorList = []
          response.data['color_list'].forEach((r, i) => {
            this.colorList.push({
              'cluster': i + 1,
              'color_list': r,
              'histogram': response.data['histogram'][i]
            })
          })
        })
        .catch(error => {
          this.loading = false
          console.log(error)
          alert('File Upload Failed.')
        })
    },
    createImage (file) {
      const reader = new FileReader()
      reader.onload = e => {
        this.uploadFile = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }
}
</script>

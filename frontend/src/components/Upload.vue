<template>
  <div class="file-upload">
    <h3>File Upload</h3>
        <div class="loading" v-show="loading">
          <div class="loading__inner">
            <h3>Uploading...</h3>
            <img src="@/assets/icon_loader_f_ww_01_s1.gif">
          </div>
        </div>
        <div class="file-upload__form">
          <form method="post" enctype="multipart/form-data">
            <p>
                <input @change="selectedFile" type="file" name ="file" id="file">
            </p>
            <p>
              <button @click="upload" type="button">Upload</button>
            </p>
          </form>
          <div class="file-upload__form__prev">
            <img
              v-show="uploadFile"
              :src="uploadFile"
              alt=""
            />
          </div>
        </div>
        <div class="color-bar">
          <div v-for="row in colorList" v-bind:key="row.index" v-bind:style="'background-color: rgb(' + row[0] + ',' + row[1] + ',' + row[2] + ')'"></div>
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
      loading: false,
      colorList: []
    }
  },
  methods: {
    selectedFile (e) {
      let files = e.target.files
      console.log(files)
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
      // loading on
      this.loading = true
      axios.post('/uploads', params, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          this.loading = false
          alert('File Upload Success!')
          console.log(response)
          this.colorList = response.data['color_list']
          // redirect ro list page
          // document.location = '/list'
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

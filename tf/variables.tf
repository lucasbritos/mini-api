variable "AUTH_REQUEST" {
  type        = string
  default     = "True"
}

variable "SERVER_DEBUG" {
  type        = string
  default     = "False"
}

variable "REMOTE_JWKS_ENDPOINT" {
  type        = string
  nullable    = true
  default     = null
}

variable "LOGGING_LEVEL" {
  type        = string
  default     = "INFO"
}
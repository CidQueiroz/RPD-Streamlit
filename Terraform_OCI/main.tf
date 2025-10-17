# Bloco 1: Define variáveis locais para fácil referência
locals {
  tenancy_ocid     = "ocid1.tenancy.oc1..aaaaaaaaqkgspzxljtpsdeyudwww6acp6foze7r6iuxyrns6yvt5hnr667ra"
  user_ocid        = "ocid1.user.oc1..aaaaaaaafedxtjtkevga56dibemmwfqhwm7wnngwdrbwucngyqwbjuafyssa"
  fingerprint      = "be:f4:b6:1d:14:e0:d0:27:61:ed:1b:f4:ac:1e:95:86"
  private_key_path = ".oci/oci_api_key.pem"
  region           = "sa-saopaulo-1"                
}

# Bloco 2: Configura o provedor da Oracle Cloud (OCI)
provider "oci" {
  tenancy_ocid     = local.tenancy_ocid
  user_ocid        = local.user_ocid
  fingerprint      = local.fingerprint
  private_key_path = local.private_key_path
  region           = local.region
}

# Bloco 3: Encontra o ID do compartimento raiz (AGORA CORRIGIDO)
data "oci_identity_compartment" "root" {
  id = local.tenancy_ocid
}

# Bloco 4: Encontra a imagem mais recente do Ubuntu
data "oci_core_images" "ubuntu" {
  compartment_id           = data.oci_identity_compartment.root.id
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "24.04"
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

# Bloco 5: A "Planta Baixa" da sua Máquina Virtual
resource "oci_core_instance" "streamlit_vm" {
  # Detalhes básicos
  display_name   = "Servidor-Streamlit-Terraform"
  compartment_id = data.oci_identity_compartment.root.id

  # Localização (aqui ele tentará o AD-1, mude se necessário)
  availability_domain = "umkt:SA-SAOPAULO-1-AD-1" #

  # Formato "Always Free"
  shape = "VM.Standard.A1.Flex"
  shape_config {
    ocpus         = 1
    memory_in_gbs = 6
  }

  # Imagem e Rede
  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.ubuntu.images[0].id
  }

  create_vnic_details {
    subnet_id        = "ocid1.subnet.oc1.sa-saopaulo-1.aaaaaaaakutxchmqlzys4fkpjtn762fcj44kglgx76zwku33yyyl2ljyoaga"
    assign_public_ip = true
  }

  # Chave SSH para acesso
  metadata = {
    ssh_authorized_keys = file("ssh-key-2025-09-10.key.pub")
  }
}

# Bloco 6: Mostra o IP Público no final
output "ip_publico" {
  value = oci_core_instance.streamlit_vm.public_ip
}
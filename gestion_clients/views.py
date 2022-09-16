from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import is_auth, allowed_users
from .forms import *
from .forms import CreatUserForm
from .models import *
from .validators import *

nav_elements = [
    {"label": "Acceuil", "link": "home"},
    {"label": "Navire", "link": "navire"},
    {"label": "Mareyeur", "link": "mareyeur"},
]

multiupload = ("armateur_ou_RC", "acte_cession_delegation", "divers_documents", "rc_ou_statut", "acte_de_cession")


def register(request):
    form = CreatUserForm()
    return render(request, "gestion_clients/register.html", {"form": form})


def dec_list(perm=None):
    if None:
        return login_required(login_url="login")
    else:
        return [login_required(login_url="login"), allowed_users(perm)]


@method_decorator(is_auth, name='dispatch')
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({"placeholder": "Nom d'utilisateur...", "class": "form-control"})
        form.fields['password'].widget.attrs.update({"placeholder": "Mot de passe...", "class": "form-control"})
        return render(request, "gestion_clients/login.html", {"form": form})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.warning(request, "Nom d'utilisateur ou mot de pass incorrecte")
            return self.get(request)


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def home(request):
    print(request.readlines())
    return render(request, "gestion_clients/index.html", {"nav": nav_elements, "nb_arma": Navire.objects.count(),
                                                          "nb_mara": Mareyeur.objects.count(),
                                                          "nb_doc": Document.objects.count()})


@method_decorator(dec_list(['gestion_clients.view_navire']), name='dispatch')
class NavireView(View):
    def get(self, request):
        return render(request, "gestion_clients/search.html",
                      {"nav": nav_elements, "link": "create_navire", "name": "Navire"})

    def post(self, request):
        if request.POST["search"]:
            try:
                navire = Navire.objects.get(pk=request.POST["search"])
                return redirect(navire)
            except:
                messages.error(request, "Navire introuvable")
                return render(request, "gestion_clients/search.html",
                              {"nav": nav_elements, "link": "create_navire", "name": "Navire"})
        else:
            messages.error(request, "Le champ est obligatoire")
            return render(request, "gestion_clients/search.html",
                          {"nav": nav_elements, "link": "create_navire", "name": "Navire"})


@method_decorator(dec_list(['gestion_clients.add_navire']), name='dispatch')
class CreateNavireView(View):
    def get(self, request):
        return render(request, "gestion_clients/create.html",
                      {"nav": nav_elements, "name": "Navire", "form": NavireForm(), "multiupload": multiupload})

    def post(self, request):
        form = NavireForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                navire = Navire(matricule=request.POST["matricule"])
                try:
                    navire.save()
                except:
                    messages.error(request, "Le navire a été deja enregistré")
                    return render(request, "gestion_clients/create.html",
                                  {"nav": nav_elements, "name": "Navire", "form": form, "multiupload": multiupload})
                for key, _ in request.FILES.items():
                    [validate_type(file) for file in request.FILES.getlist(key)]
                ActeNationaliteNavire(file=request.FILES.get("acte_de_nationalite"), client=navire).save()
                for file in request.FILES.getlist("armateur_ou_RC"):
                    ArmateurRcNavire(file=file, client=navire).save()
                for file in request.FILES.getlist("acte_cession_delegation"):
                    ActeCessionNavire(file=file, client=navire).save()
                for file in request.FILES.getlist("divers_documents"):
                    DiversNavire(file=file, client=navire).save()
                return redirect(navire)
            except:
                messages.error(request, "Type de fichiers non pris en charge")
                return render(request, "gestion_clients/create.html",
                              {"nav": nav_elements, "name": "Navire", "form": form, "multiupload": multiupload})


def update_files(request, up_list):
    for key, value in up_list.items():
        a, b = str.split(key, "-")
        doc = Document.objects.get(pk=int(a))
        try:
            validate_type(value)
            doc.file = value
            doc.save()
        except ValidationError:
            messages.error(request, "Type de fichiers non pris en charge")


def dell(del_list):
    for key, value in del_list.items():
        if not key.endswith("delete"):
            continue
        a, b = str.split(key, "-")
        doc = Document.objects.get(pk=int(a))
        doc.file = None
        doc.save()


@method_decorator(dec_list(['gestion_clients.view_navire']), name='dispatch')
class NavireDetailsView(View):
    def get(self, request, slug):
        navire = Navire.objects.get(slug=slug)
        ide = navire.client_ptr_id
        acte_natio = ActeNationaliteNavire.objects.filter(client=ide).values("id", "date_creation", "date_modification")
        arma_rc = ArmateurRcNavire.objects.filter(client=ide).values("id", "date_creation", "date_modification")
        acte_cession = ActeCessionNavire.objects.filter(client=ide).values("id", "date_creation", "date_modification")
        divers = DiversNavire.objects.filter(client=ide).values("id", "date_creation", "date_modification")
        tup = ("Acte National", "Armateur ou RC", "Acte de cession", "Divers")
        acte = list(zip(tup, (acte_natio, arma_rc, acte_cession, divers)))
        for _, b in acte:
            for i in b:
                i["form"] = DocumentDetailsForm(id=i["id"], prefix=i["id"])

        return render(request, "gestion_clients/details.html", {
            "nav": nav_elements,
            "who": "du navire " + str(navire.matricule),
            "table_header": ["Id", "Date de creation", "Dernier date de modification"],
            "acte": acte,
            "link": "create_navire",
            "link_delete": "delete_navire",
            "update": request.user.has_perms('gestion_clients.change_navire'),
            "id": slug,
            "who_class": "navire"
        })

    def post(self, request, slug):
        dell(request.POST)
        update_files(request, request.FILES)
        messages.success(request, "Les information du navire ont été modifiées avec succes")
        return self.get(request, slug)


@method_decorator(dec_list(['gestion_clients.view_mareyeur']), name='dispatch')
class MareyeurView(View):
    def get(self, request):
        return render(request, "gestion_clients/search.html",
                      {"nav": nav_elements, "link": "create_mareyeur", "name": "Mareyeur"})

    def post(self, request):
        if request.POST["search"]:
            try:
                mareyeur = Mareyeur.objects.get(pk=request.POST["search"])
                return redirect(mareyeur)
            except:
                messages.error(request, "Mareyeur introuvable")
                return render(request, "gestion_clients/search.html",
                              {"nav": nav_elements, "name": "Mareyeur", "link": "create_mareyeur"})
        else:
            messages.error(request, "Le champ est obligatoire !")
            return render(request, "gestion_clients/search.html",
                          {"nav": nav_elements, "name": "Mareyeur", "link": "create_mareyeur"})


@method_decorator(dec_list(['gestion_clients.add_mareyeur']), name='dispatch')
class CreateMareyeurView(View):
    def get(self, request):
        return render(request, "gestion_clients/create.html",
                      {"nav": nav_elements, "name": "Mareyeur", "form": MareyeurForm(), "multiupload": multiupload})

    def post(self, request):
        form = MareyeurForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                mareyeur = Mareyeur(code_national=request.POST["code_national"])
                try:
                    mareyeur.save()
                except:
                    messages.error(request, "Le mareyeur a été deja enregistré")
                    return render(request, "gestion_clients/create.html",
                                  {"nav": nav_elements, "name": "Mareyeur", "form": form, "multiupload": multiupload})
                for key, _ in request.FILES.items():
                    [validate_type(file) for file in request.FILES.getlist(key)]
                CinMareyeur(file=request.FILES.get("cin_mareyeur"), client=mareyeur).save()
                for file in request.FILES.getlist("rc_ou_statut"):
                    RcStatutMareyeur(file=file, client=mareyeur).save()
                for file in request.FILES.getlist("acte_de_cession"):
                    ActeCessionMareyeur(file=file, client=mareyeur).save()
                CarteAutorisationMareyeur(file=request.FILES.get("carte_marayeur_ou_autorisation"),
                                          client=mareyeur).save()
                for file in request.FILES.getlist("divers_documents"):
                    DiversMareyeur(file=file, client=mareyeur).save()
                return redirect(mareyeur)
            except:
                messages.error(request, "Type de fichiers non pris en charge")
                return render(request, "gestion_clients/create.html",
                              {"nav": nav_elements, "name": "Mareyeur", "form": form, "multiupload": multiupload})


@method_decorator(dec_list(['gestion_clients.view_mareyeur']), name='dispatch')
class MareyeurDetailsView(View):
    def get(self, request, slug):
        mareyeur = Mareyeur.objects.get(slug=slug)
        ide = mareyeur.client_ptr_id
        cin_mareyeur = CinMareyeur.objects.filter(client=ide).values("id", "date_creation", "date_modification")
        rc_ou_statut = RcStatutMareyeur.objects.filter(client=ide).values("id", "date_creation", "date_modification")
        acte_de_cession = ActeCessionMareyeur.objects.filter(client=ide).values("id", "date_creation",
                                                                                "date_modification")
        carte_marayeur_ou_autorisation = CarteAutorisationMareyeur.objects.filter(client=ide).values("id",
                                                                                                     "date_creation",
                                                                                                     "date_modification")
        divers_documents = DiversMareyeur.objects.filter(client=ide).values("id", "date_creation", "date_modification")
        tup = ("Cin", "Rc ou statut", "Acte de cession", "Carte mareyeur ou autorisation", "Diver document")
        acte = list(
            zip(tup, (cin_mareyeur, rc_ou_statut, acte_de_cession, carte_marayeur_ou_autorisation, divers_documents)))
        for _, b in acte:
            for i in b:
                i["form"] = DocumentDetailsForm(id=i["id"], prefix=i["id"])

        return render(request, "gestion_clients/details.html", {
            "nav": nav_elements,
            "who": "du mareyeur " + str(mareyeur.code_national),
            "table_header": ["Id", "Date de creation", "Dernier date de modification"],
            "acte": acte,
            "link": "create_mareyeur",
            "link_delete": "delete_mareyeur",
            "update": request.user.has_perms('gestion_clients.change_mareyeur'),
            "id": slug,
            "who_class": "mareyeur"
        })

    def post(self, request, slug):
        dell(request.POST)
        update_files(request, request.FILES)
        messages.success(request, "Les information du mareyeur ont été modifiées avec succes")
        return self.get(request, slug)


label_dict = {

    "cin": "carte national",
    "ass": "assurance",
    "rc": "recue"
}


def who(id, sm):
    if id == "navire":
        return "du navire " + str(sm)
    elif id == "marayeur":
        return "du marayeur " + str(sm)
    else:
        return None


@method_decorator(dec_list(['gestion_clients.view_document']), name='dispatch')
class DocumentView(View):
    def get(self, request, id):
        data = Document.objects.get(pk=id)
        return render(request, "gestion_clients/file.html", {
            "nav": nav_elements,
            "who": who("navire", data.client_id),
            "upload_date": data.date_modification,
            "file": data.file
        })


@login_required(login_url="login")
@allowed_users(['gestion_clients.delete_navire'])
def delete_navire(request, slug):
    Navire.objects.get(pk=slug).delete()
    messages.success(request, "Le navire a été supprimé avec succes")
    return redirect("navire")


@login_required(login_url="login")
@allowed_users(['gestion_clients.delete_mareyeur'])
def delete_mareyeur(request, slug):
    Mareyeur.objects.get(pk=slug).delete()
    messages.success(request, "Le mareyeur a été supprimé avec succes")
    return redirect("mareyeur")

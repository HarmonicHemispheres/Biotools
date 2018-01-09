#!/usr/local/bin/perl
use Bio::EnsEMBL::Registry;

my $registry = 'Bio::EnsEMBL::Registry';

$registry->load_registry_from_db(
    -host => 'ensembldb.ensembl.org',  # alternatively 'useastdb.ensembl.org'
    -user => 'anonymous'
);

# first you have to get a GeneMember object. In case of homology is a gene, in 
# case of family it can be a gene or a protein

my $gene_member_adaptor = Bio::EnsEMBL::Registry->get_adaptor('Multi', 'compara', 'GeneMember');
my $gene_member = $gene_member_adaptor->fetch_by_stable_id('ENSG00000004059');

# then you get the homologies where the member is involved

my $homology_adaptor = Bio::EnsEMBL::Registry->get_adaptor('Multi', 'compara', 'Homology');
my $homologies = $homology_adaptor->fetch_all_by_Member($gene_member);

# That will return a reference to an array with all homologies (orthologues in
# other species and paralogues in the same one)
# Then for each homology, you can get all the Members implicated

foreach my $homology (@{$homologies}) {
  # You will find different kind of description
  # see ensembl-compara/docs/docs/schema_doc.html for more details

  print $homology->description," ", $homology->taxonomy_level,"\n";

  # And if they are defined dN and dS related values

  print " dn ", $homology->dn,"\n";
  print " ds ", $homology->ds,"\n";
  print " dnds_ratio ", $homology->dnds_ratio,"\n";
}

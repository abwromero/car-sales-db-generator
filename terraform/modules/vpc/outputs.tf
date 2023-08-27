output "vpc_id" {
  value = aws_vpc.main_vpc.id
}

output "vpc_cidr_block" {
  value = aws_vpc.main_vpc.cidr_block
}

output "public_subnets_ids" {
  value = aws_subnet.public.*.id
}

output "route_table_public_id" {
  value = aws_route_table.public.id
}

output "azs" {
  value = aws_subnet.public[*].availability_zone
}